"""Small assertion helpers used by the tests. You never need to edit this file."""
from __future__ import annotations

import math


def expect(actual, expected, what: str = "result") -> None:
    if actual != expected:
        raise AssertionError(f"{what}\n    expected: {expected!r}\n    got:      {actual!r}")


def _close(a, b, tol: float) -> bool:
    return isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def expect_close(actual, expected, what: str = "result", tol: float = 1e-6) -> None:
    """Like expect(), for floats or lists of floats (small rounding differences are fine)."""
    if isinstance(expected, (list, tuple)):
        ok = (isinstance(actual, (list, tuple)) and len(actual) == len(expected)
              and all(_close(a, b, tol) for a, b in zip(actual, expected)))
    else:
        ok = _close(actual, expected, tol)
    if not ok:
        raise AssertionError(f"{what}\n    expected: {expected!r}  (± {tol})\n    got:      {actual!r}")


def expect_raises(error: type[Exception], fn, *args, what: str = "", **kwargs) -> None:
    try:
        fn(*args, **kwargs)
    except error:
        return
    except NotImplementedError:
        raise
    except Exception as e:
        raise AssertionError(f"{what}\n    expected {error.__name__} to be raised\n    got {type(e).__name__}: {e}")
    raise AssertionError(f"{what}\n    expected {error.__name__} to be raised, but nothing was raised")
