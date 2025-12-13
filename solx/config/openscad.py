"""OpenSCAD configuration utilities.

This module provides:
- OpenSCADNotFoundError: exception when OpenSCAD executable is not found
- get_openscad_path: locate OpenSCAD executable on the system
"""
# %%
import os
import shutil
from pathlib import Path


class OpenSCADNotFoundError(RuntimeError):
    """Exception raised when OpenSCAD executable is not found on the system."""
    pass


def get_openscad_path() -> str:
    """Locate OpenSCAD executable on the system.

    Returns:
        str: Path to the OpenSCAD executable.

    Raises:
        OpenSCADNotFoundError: If OpenSCAD executable is not found.
    """
    # 1. 環境変数
    env = os.environ.get("OPENSCAD_PATH")
    if env:
        return env

    # 2. PATH
    path = shutil.which("openscad")
    if path:
        return path

    # 3. Windows fallback
    if os.name == "nt":
        candidates = [
            r"C:\Program Files\OpenSCAD\openscad.exe",
            r"C:\Program Files (x86)\OpenSCAD\openscad.exe",
        ]
        for c in candidates:
            if Path(c).exists():
                return c

    raise OpenSCADNotFoundError(
        "OpenSCAD not found.\nInstall OpenSCAD or set OPENSCAD_PATH."
    )
# %%
