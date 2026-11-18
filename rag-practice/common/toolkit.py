"""Reuse your own solutions from earlier modules.

    from toolkit import module

    vectors = module(7)                  # loads modules/07_*/exercise.py
    vectors.cosine([1, 0], [1, 1])       # calls YOUR cosine()

This is how real RAG code is built: small tested functions, glued together.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_MODULES = Path(__file__).resolve().parent.parent / "modules"
_cache: dict[int, object] = {}


def module(number: int):
    if number in _cache:
        return _cache[number]
    for d in sorted(_MODULES.iterdir()):
        if d.is_dir() and d.name[:2].isdigit() and int(d.name[:2]) == number:
            spec = importlib.util.spec_from_file_location(f"your_module_{number:02d}", d / "exercise.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _cache[number] = mod
            return mod
    raise ValueError(f"There is no module {number}.")
