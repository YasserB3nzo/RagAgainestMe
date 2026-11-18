#!/usr/bin/env python3
"""Local web interface for RAG practice.

    python3 server.py            then open http://localhost:8765 (opens automatically)
    python3 server.py 9000       use another port

Your code is saved straight into modules/*/exercise.py, so the website and
`python3 rag.py` always show the same thing.
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import textwrap
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
MODULES_DIR = ROOT / "modules"
WEB_DIR = ROOT / "web"
ORIGINALS = ROOT / ".original"  # untouched copies of each exercise.py, used by "Reset"
PROGRESS_FILE = ROOT / ".progress.json"

BANNER_RULE = re.compile(r"^\s*# ─{5,}")
BANNER_TITLE = re.compile(r"^\s*# Problem (\d+) · (\w+)\s*(?:\((.+?)\))?")
LOCK = threading.Lock()

sys.path.insert(0, str(ROOT / "common"))
from playground import STARTERS  # noqa: E402  (per-problem playground starter code)
EXEC_TIMEOUT = 10        # seconds before a playground run is stopped
EXEC_MAX_OUTPUT = 100_000  # characters of output sent back to the browser

# Runs in a separate Python process: load exercise.py, then run the playground code
# in the same namespace, so every function from the file is available by name.
PLAYGROUND_RUNNER = r"""
import sys, traceback
module_dir, common_dir = sys.argv[1], sys.argv[2]
sys.path[:0] = [module_dir, common_dir]
path = module_dir + "/exercise.py"
scope = {"__name__": "exercise", "__file__": path}

def fail(stage):
    kind, err, tb = sys.exc_info()
    while tb is not None and tb.tb_frame.f_code.co_filename == "<string>":
        tb = tb.tb_next  # hide this runner's own frames
    print(stage, file=sys.stderr)
    traceback.print_exception(kind, err, tb)
    sys.exit(1)

try:
    exec(compile(open(path, encoding="utf-8").read(), "exercise.py", "exec"), scope)
except SystemExit:
    raise
except BaseException:
    fail("exercise.py could not be loaded:")
scope["__name__"] = "__main__"
try:
    exec(compile(sys.stdin.read(), "playground", "exec"), scope)
except SystemExit:
    raise
except BaseException:
    fail("")
"""


# ---------------------------------------------------------------- files

def module_dir(number: int) -> Path:
    for d in sorted(MODULES_DIR.iterdir()):
        if d.is_dir() and d.name[:2].isdigit() and int(d.name[:2]) == number:
            return d
    raise KeyError(f"no module {number}")


def ensure_originals() -> None:
    ORIGINALS.mkdir(exist_ok=True)
    for d in sorted(MODULES_DIR.iterdir()):
        target = ORIGINALS / f"{d.name}.py"
        if d.is_dir() and d.name[:2].isdigit() and not target.exists():
            shutil.copy(d / "exercise.py", target)


def regions(lines: list[str]) -> dict[str, dict]:
    """Find each problem's editable region: the lines between its banner and the next banner."""
    found = {}
    for i, line in enumerate(lines):
        m = BANNER_TITLE.match(line)
        if m and i + 1 < len(lines) and BANNER_RULE.match(lines[i + 1]):
            found[m.group(2)] = {"start": i + 2, "number": int(m.group(1)), "difficulty": (m.group(3) or "").strip()}
    ordered = sorted(found.values(), key=lambda r: r["start"])
    for r in ordered:
        r["end"] = len(lines)
        for j in range(r["start"], len(lines) - 1):
            if BANNER_RULE.match(lines[j]) and BANNER_TITLE.match(lines[j + 1]):
                r["end"] = j
                break
    return found


def _trailing_blanks(chunk: list[str]) -> int:
    n = 0
    for line in reversed(chunk):
        if line.strip():
            break
        n += 1
    return n


def find_region(lines: list[str], problem: str, path: Path) -> dict:
    found = regions(lines)
    if problem not in found:
        raise ValueError(f"Can't find the '# Problem N · {problem}' banner in {path.parent.name}/{path.name}. "
                         "The website uses those comment lines to know where each problem starts; "
                         "put the banner back (copy it from .original/) and reload.")
    return found[problem]


def read_code(path: Path, problem: str) -> str:
    lines = path.read_text(encoding="utf-8").split("\n")
    r = find_region(lines, problem, path)
    chunk = lines[r["start"]:r["end"]]
    return "\n".join(chunk[:len(chunk) - _trailing_blanks(chunk)])


def write_code(number: int, problem: str, code: str, source: Path | None = None) -> None:
    path = module_dir(number) / "exercise.py"
    with LOCK:
        lines = path.read_text(encoding="utf-8").split("\n")
        r = find_region(lines, problem, path)
        blanks = max(_trailing_blanks(lines[r["start"]:r["end"]]), 1)
        new = (read_code(source, problem) if source else code).rstrip().split("\n")
        lines[r["start"]:r["end"]] = new + [""] * blanks
        path.write_text("\n".join(lines), encoding="utf-8")


def docstrings(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {n.name: ast.get_docstring(n) or "" for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def example_call(doc: str, name: str) -> str | None:
    """Pull the first `name(...)` call out of a docstring's Example section, if it parses."""
    text = doc[doc.find("Example"):] if "Example" in doc else ""
    j = text.find(name + "(")
    while j > 0 and (text[j - 1].isalnum() or text[j - 1] == "_"):
        j = text.find(name + "(", j + 1)
    if j < 0:
        return None
    depth, quote = 0, None
    for e in range(j + len(name), len(text)):
        ch = text[e]
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                first, *rest = text[j:e + 1].split("\n")
                call = "\n".join([first] + textwrap.indent(textwrap.dedent("\n".join(rest)), "    ").split("\n")) \
                    if rest else first
                try:
                    ast.parse(call)
                except SyntaxError:
                    return None
                return call
    return None


def starter(number: int, name: str, doc: str) -> str:
    """Default playground code for a problem."""
    custom = STARTERS.get(f"{number:02d}/{name}")
    if custom:
        return custom
    call = example_call(doc, name)
    head = f"# Your code from exercise.py is already loaded: call {name}() with any input.\n"
    return head + (f"print({call})\n" if call else f"print({name}())\n")


def load_hints(number: int) -> dict[str, list[str]]:
    scope: dict = {}
    exec((module_dir(number) / "hints.py").read_text(encoding="utf-8"), scope)
    return scope["HINTS"]


def read_progress() -> dict:
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def run_rag(*args: str) -> object:
    done = subprocess.run([sys.executable, str(ROOT / "rag.py"), *args], cwd=ROOT,
                          capture_output=True, text=True, timeout=180)
    if done.returncode != 0 or not done.stdout.strip():
        raise RuntimeError(done.stderr.strip() or "the test runner stopped unexpectedly")
    return json.loads(done.stdout)


# ---------------------------------------------------------------- API

def api_module(number: int) -> dict:
    d = module_dir(number)
    original = ORIGINALS / f"{d.name}.py"
    docs = docstrings(original)
    meta = regions(original.read_text(encoding="utf-8").split("\n"))
    hints = load_hints(number)
    seen = read_progress().get("hints", {})
    problems = []
    for name, r in sorted(meta.items(), key=lambda kv: kv[1]["number"]):
        problems.append({
            "name": name, "number": r["number"], "difficulty": r["difficulty"] or "easy",
            "description": docs.get(name, ""), "code": read_code(d / "exercise.py", name),
            "starter": starter(number, name, docs.get(name, "")),
            "hints_total": len(hints.get(name, [])),
            "hints": hints.get(name, [])[:seen.get(f"{d.name[:2]}/{name}", 0)],
        })
    guide = (d / "README.md").read_text(encoding="utf-8")
    return {"number": number, "title": guide.splitlines()[0].lstrip("# ").strip(), "guide": guide,
            "problems": problems}


def api_exec(number: int, scratch: str) -> dict:
    d = module_dir(number)
    started = time.perf_counter()
    try:
        done = subprocess.run([sys.executable, "-u", "-c", PLAYGROUND_RUNNER, str(d), str(ROOT / "common")],
                              input=scratch, cwd=ROOT, capture_output=True, text=True, timeout=EXEC_TIMEOUT)
        stdout, stderr, code, timed_out = done.stdout, done.stderr, done.returncode, False
    except subprocess.TimeoutExpired as e:
        decode = lambda b: b.decode("utf-8", "replace") if isinstance(b, bytes) else (b or "")
        stdout, stderr, code, timed_out = decode(e.stdout), decode(e.stderr), None, True
    return {"stdout": stdout[:EXEC_MAX_OUTPUT], "stderr": stderr[:EXEC_MAX_OUTPUT],
            "truncated": len(stdout) > EXEC_MAX_OUTPUT or len(stderr) > EXEC_MAX_OUTPUT,
            "exit_code": code, "timed_out": timed_out, "timeout": EXEC_TIMEOUT,
            "seconds": round(time.perf_counter() - started, 3)}


def api_hint(number: int, problem: str) -> dict:
    d = module_dir(number)
    hints = load_hints(number)[problem]
    progress = read_progress()
    key = f"{d.name[:2]}/{problem}"
    shown = min(progress.setdefault("hints", {}).get(key, 0) + 1, len(hints))
    progress["hints"][key] = shown
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    return {"hints": hints[:shown], "hints_total": len(hints)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data, status: int = 200) -> None:
        self._send(status, json.dumps(data).encode("utf-8"), "application/json")

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/api/status":
                return self._json(run_rag("json-status"))
            if url.path == "/api/module":
                return self._json(api_module(int(query["n"])))
            if url.path == "/api/code":
                return self._json({"code": read_code(module_dir(int(query["n"])) / "exercise.py", query["problem"])})
        except Exception as e:
            return self._json({"error": str(e)}, 500)
        name = "index.html" if url.path in ("/", "") else url.path.lstrip("/")
        file = (WEB_DIR / name).resolve()
        if WEB_DIR in file.parents and file.is_file():
            kind = {".html": "text/html", ".css": "text/css", ".js": "text/javascript"}.get(file.suffix, "text/plain")
            return self._send(200, file.read_bytes(), kind + "; charset=utf-8")
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        try:
            body = self._body()
            n = int(body["module"])
            if self.path == "/api/save":
                write_code(n, body["problem"], body["code"])
                return self._json({"ok": True})
            if self.path == "/api/run":
                if "code" in body:
                    write_code(n, body["problem"], body["code"])
                args = ["json-test", str(n)] + ([body["problem"]] if body.get("scope") != "module" else [])
                return self._json(run_rag(*args))
            if self.path == "/api/exec":
                if "code" in body:
                    write_code(n, body["problem"], body["code"])
                return self._json(api_exec(n, body.get("scratch", "")))
            if self.path == "/api/hint":
                return self._json(api_hint(n, body["problem"]))
            if self.path == "/api/reset":
                d = module_dir(n)
                write_code(n, body["problem"], "", source=ORIGINALS / f"{d.name}.py")
                return self._json({"code": read_code(d / "exercise.py", body["problem"])})
            self._json({"error": "unknown endpoint"}, 404)
        except subprocess.TimeoutExpired:
            self._json({"error": "The tests took too long to finish."}, 500)
        except Exception as e:
            self._json({"error": str(e)}, 500)


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ensure_originals()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}"
    print(f"\n  RAG practice is running at {url}\n  Press Ctrl+C to stop.\n")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")


if __name__ == "__main__":
    main()
