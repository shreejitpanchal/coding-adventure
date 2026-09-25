"""The one place the repo-relative layout is spelled out.

Every module that needs the checkout root (content, the Spring Maven
scaffold, the default data directory) imports it from here instead of
recomputing `Path(__file__).resolve().parent.parent...` on its own -- one
definition to update if the package ever moves, and one place to read to
learn where things live."""
from __future__ import annotations

from pathlib import Path

# <repo>/app/config/paths.py -> <repo>
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CONTENT_ROOT = REPO_ROOT / "content"
SPRING_SCAFFOLD_DIR = CONTENT_ROOT / "spring" / "scaffold"
