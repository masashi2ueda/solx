import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class EnvConfig:
    # Optional legacy env var. Keep compatibility but avoid hard failure when unset.
    OUTPUT_STL_DIR_PATH = os.environ.get("OUTPUT_STL_DIR_PATH")

    @classmethod
    def get_output_stl_dir_path(cls) -> str:
        """Return configured STL output directory path with a safe default.

        If OUTPUT_STL_DIR_PATH is not set, default to ./output_stl.
        """
        return cls.OUTPUT_STL_DIR_PATH or str(Path("output_stl"))
