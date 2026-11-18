#!/usr/bin/env python3
"""RAG practice: small coding problems that build the bare minimum for a RAG system.

    python rag.py                       progress overview
    python rag.py learn 4               read the guide for module 4
    python rag.py test 4                run every test in module 4
    python rag.py test 4 line_windows   run the tests for one problem
    python rag.py hint 4 line_windows   reveal the next hint for a problem
    python rag.py next                  show where to continue
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import signal
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES_DIR = ROOT / "modules"
COMMON_DIR = ROOT / "common"
PROGRESS_FILE = ROOT / ".progress.json"
TIME_LIMIT = 3  # seconds allowed per test case
CAPTURE = False  # the web interface sets this to collect print() output per test case

sys.path.insert(0, str(COMMON_DIR))

USE_COLOR = sys.stdout.isatty()


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def green(t): return paint(t, "32")
def red(t): return paint(t, "31")
def yellow(t): return paint(t, "33")
def cyan(t): return paint(t, "36")
def dim(t): return paint(t, "2")
def bold(t): return paint(t, "1")


def die(message: str) -> None:
    print(red(message))
    sys.exit(1)


# ---------------------------------------------------------------- modules

def module_dirs() -> list[Path]:
    return sorted(p for p in MODULES_DIR.iterdir() if p.is_dir() and p.name[:2].isdigit())


def find_module(arg: str) -> Path:
    try:
        number = int(arg)
    except ValueError:
        die(f"'{arg}' is not a module number. Try: python rag.py test 4")
    for d in module_dirs():
        if int(d.name[:2]) == number:
            return d
    die(f"There is no module {arg}. Modules go from 1 to {len(module_dirs())}.")


def title_of(mod_dir: Path) -> str:
    first = (mod_dir / "README.md").read_text(encoding="utf-8").splitlines()[0]
    return first.lstrip("# ").strip()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- running tests

class TimeLimit(BaseException):  # BaseException so a learner's `except Exception` can't swallow it
    pass


def _on_alarm(signum, frame):
    raise TimeLimit()


def _frames(error: BaseException):
    return traceback.extract_tb(error.__traceback__)


def describe_error(error: BaseException, ex_path: Path) -> str:
    lines = [f.lineno for f in _frames(error) if Path(f.filename) == ex_path]
    where = f" (exercise.py, line {lines[-1]})" if lines else ""
    return f"{type(error).__name__}: {error}{where}"


def run_case(fn, ex, ex_path: Path) -> tuple[str, str, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out) if CAPTURE else contextlib.nullcontext():
        status, message = _run_case(fn, ex, ex_path)
    return status, message, out.getvalue()


def _run_case(fn, ex, ex_path: Path) -> tuple[str, str]:
    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _on_alarm)
        signal.setitimer(signal.ITIMER_REAL, TIME_LIMIT)
    try:
        fn(ex)
        return "pass", ""
    except NotImplementedError as e:
        last = _frames(e)[-1] if _frames(e) else None
        if last and Path(last.filename) != ex_path and MODULES_DIR in Path(last.filename).parents:
            other = Path(last.filename).parent.name
            return "blocked", f"this uses {last.name}() from modules/{other}, which isn't solved yet"
        return "todo", ""
    except TimeLimit:
        return "fail", f"took longer than {TIME_LIMIT}s. Is there an infinite loop?"
    except AssertionError as e:
        return "fail", str(e) or "a check failed"
    except Exception as e:  # any bug in the learner's code
        return "error", describe_error(e, ex_path)
    finally:
        if use_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)


def run_module(mod_dir: Path, only: str | None = None):
    """Return (problems, results, load_error). results: problem -> [(case, status, message)]."""
    ex_path = mod_dir / "exercise.py"
    tests = load(mod_dir / "tests.py", f"tests_{mod_dir.name}")
    problems = list(tests.PROBLEMS)
    try:
        ex = load(ex_path, f"exercise_{mod_dir.name}")
    except NotImplementedError as e:
        return problems, {}, describe_error(e, ex_path)
    except Exception as e:
        return problems, {}, describe_error(e, ex_path)

    results: dict[str, list] = {name: [] for name, _ in problems}
    for attr, fn in vars(tests).items():
        if not (attr.startswith("test_") and callable(fn)):
            continue
        problem, _, case = attr[5:].partition("__")
        if only and problem != only:
            continue
        status, message, output = run_case(fn, ex, ex_path)
        results.setdefault(problem, []).append((case, status, message, output))
    if only:
        results = {only: results.get(only, [])}
    return problems, results, None


def problem_state(cases) -> str:
    statuses = {s for _, s, *_ in cases}
    if not cases or statuses <= {"todo"}:
        return "todo"
    if statuses == {"pass"}:
        return "solved"
    if "blocked" in statuses:
        return "blocked"
    return "started"


# ---------------------------------------------------------------- progress file

def read_progress() -> dict:
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def write_progress(data: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- commands

def cmd_status() -> None:
    print(bold("\nRAG practice") + dim("  ·  solve the problems in modules/*/exercise.py\n"))
    for d in module_dirs():
        problems, results, load_error = run_module(d)
        total = len(problems)
        solved = sum(problem_state(results.get(name, [])) == "solved" for name, _ in problems)
        bar = "█" * solved + "░" * (total - solved)
        if load_error:
            mark, note = red("✘"), red("exercise.py does not load: " + load_error)
        elif solved == total:
            mark, note = green("✔"), green("done")
        elif solved or any(problem_state(results.get(n, [])) != "todo" for n, _ in problems):
            mark, note = yellow("●"), f"{solved}/{total} problems"
        else:
            mark, note = dim("○"), dim("not started")
        print(f"  {mark} {d.name[:2]}  {title_of(d).split('·', 1)[-1].strip():<38} {cyan(bar)}  {note}")
    print(dim("\n  python rag.py next     to see where to continue\n"))


def cmd_test(arg: str, only: str | None = None) -> None:
    d = find_module(arg)
    problems, results, load_error = run_module(d, only)
    print(bold(f"\n{title_of(d)}\n"))
    if load_error:
        print(red(f"  exercise.py could not be loaded:\n    {load_error}\n"))
        return
    known = {name for name, _ in problems}
    if only and only not in known:
        die(f"No problem called '{only}' in this module. Problems: {', '.join(n for n, _ in problems)}")

    first_stuck = None
    for name, _ in problems:
        if only and name != only:
            continue
        cases = results.get(name, [])
        passed = sum(s == "pass" for _, s, *_ in cases)
        state = problem_state(cases)
        label = f"{name:<24}"
        if state == "solved":
            print(f"  {green('✔')} {label} {green(f'{passed}/{len(cases)} tests')}")
        elif state == "todo":
            print(f"  {dim('○')} {label} {dim('not started')}")
            first_stuck = first_stuck or name
        else:
            colour = yellow if state == "blocked" else red
            print(f"  {colour('✘')} {label} {colour(f'{passed}/{len(cases)} tests')}")
            for case, status, message, *_ in cases:
                if status != "pass":
                    print(dim(f"      test '{case}':"))
                    for line in message.splitlines():
                        print(f"      {line}")
                    break
            first_stuck = first_stuck or name

    number = int(d.name[:2])
    if first_stuck is None:
        if number < len(module_dirs()):
            print(green(f"\n  Module complete. Next: python rag.py learn {number + 1}\n"))
        else:
            print(green("\n  Every module is complete. You have built a tiny RAG retriever from scratch.\n"))
    else:
        print(dim(f"\n  Stuck? python rag.py hint {number} {first_stuck}\n"))


def cmd_hint(arg: str, problem: str | None) -> None:
    d = find_module(arg)
    hints = load(d / "hints.py", f"hints_{d.name}").HINTS
    if not problem:
        die(f"Which problem? python rag.py hint {int(d.name[:2])} <problem>\nProblems: {', '.join(hints)}")
    if problem not in hints:
        die(f"No problem called '{problem}'. Problems: {', '.join(hints)}")
    progress = read_progress()
    key = f"{d.name[:2]}/{problem}"
    seen = progress.setdefault("hints", {}).get(key, 0)
    total = len(hints[problem])
    shown = min(seen + 1, total)
    progress["hints"][key] = shown
    write_progress(progress)

    print(bold(f"\nHints for {problem}\n"))
    for i, text in enumerate(hints[problem][:shown], 1):
        tag = cyan(f"  Hint {i}/{total}")
        print(f"{tag}  {text}\n" if i == shown else dim(f"  Hint {i}/{total}  {text}\n"))
    if shown == total:
        print(dim("  That was the last hint. Reread the guide, add print() calls, then run the tests again.\n"))
    else:
        print(dim(f"  Run the same command again for hint {shown + 1}.\n"))


def cmd_learn(arg: str) -> None:
    d = find_module(arg)
    for line in (d / "README.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            print(bold(cyan(line)))
        else:
            print(line)
    print(dim(f"\n  Then open modules/{d.name}/exercise.py and run: python rag.py test {int(d.name[:2])}\n"))


def cmd_next() -> None:
    for d in module_dirs():
        problems, results, load_error = run_module(d)
        states = [problem_state(results.get(n, [])) for n, _ in problems]
        if load_error or any(s != "solved" for s in states):
            number = int(d.name[:2])
            print(bold(f"\nContinue with {title_of(d)}\n"))
            for (name, summary), state in zip(problems, states):
                mark = {"solved": green("✔"), "todo": dim("○")}.get(state, yellow("●"))
                print(f"  {mark} {name:<24} {dim(summary)}")
            steps = [("Edit", f"modules/{d.name}/exercise.py"), ("Check", f"python rag.py test {number}")]
            if all(s == "todo" for s in states):
                steps.insert(0, ("Read the guide", f"python rag.py learn {number}"))
            print()
            for i, (label, action) in enumerate(steps, 1):
                print(f"  {i}. {label + ':':<16} {action}")
            print()
            return
    print(green("\nEvery module is solved. Next stop: step 01 of your build plan.\n"))


def _problem_json(name, summary, cases):
    return {"name": name, "summary": summary, "state": problem_state(cases),
            "passed": sum(s == "pass" for _, s, *_ in cases), "total": len(cases),
            "cases": [{"case": c, "status": s, "message": m, "output": o} for c, s, m, o in cases]}


def cmd_json_status() -> None:
    """Machine-readable progress, used by the web interface (server.py)."""
    out = []
    with contextlib.redirect_stdout(io.StringIO()):  # keep stray print() calls out of the JSON
        for d in module_dirs():
            problems, results, load_error = run_module(d)
            out.append({"number": int(d.name[:2]), "dir": d.name, "title": title_of(d), "load_error": load_error,
                        "problems": [_problem_json(n, s, results.get(n, [])) for n, s in problems]})
    print(json.dumps(out))


def cmd_json_test(arg: str, only: str | None = None) -> None:
    d = find_module(arg)
    with contextlib.redirect_stdout(io.StringIO()):
        problems, results, load_error = run_module(d, only)
    print(json.dumps({"number": int(d.name[:2]), "title": title_of(d), "load_error": load_error,
                      "problems": [_problem_json(n, s, results.get(n, [])) for n, s in problems
                                   if not only or n == only]}))


def main(argv: list[str]) -> None:
    global CAPTURE
    if argv and argv[0].startswith("json-"):
        CAPTURE = True
    if argv and argv[0] == "json-status":
        cmd_json_status()
    elif argv and argv[0] == "json-test" and len(argv) >= 2:
        cmd_json_test(argv[1], argv[2] if len(argv) > 2 else None)
    elif not argv or argv[0] in {"status", "s"}:
        cmd_status()
    elif argv[0] in {"test", "t"} and len(argv) >= 2:
        cmd_test(argv[1], argv[2] if len(argv) > 2 else None)
    elif argv[0] in {"hint", "h"} and len(argv) >= 2:
        cmd_hint(argv[1], argv[2] if len(argv) > 2 else None)
    elif argv[0] in {"learn", "l"} and len(argv) >= 2:
        cmd_learn(argv[1])
    elif argv[0] in {"next", "n"}:
        cmd_next()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
