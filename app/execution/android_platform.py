"""Detects whether this process is running on Android.

`sys.getandroidapilevel` is a real, Android-only attribute CPython's own
Android port adds to the `sys` module specifically for this purpose --
it doesn't exist on any other platform, so `hasattr` is a reliable,
dependency-free check with no need to parse `platform.system()` (which
reports "Linux" on Android, same as a real Linux desktop, and so can't
distinguish the two on its own)."""
from __future__ import annotations

import sys


def is_android() -> bool:
    return hasattr(sys, "getandroidapilevel")
