import os
import sys
import types

# solx.config.env reads this at import time via os.environ[...].
os.environ.setdefault("OUTPUT_STL_DIR_PATH", "/tmp")


# Allow importing solx.config.env even when python-dotenv is not installed.
if "dotenv" not in sys.modules:
	dotenv_stub = types.ModuleType("dotenv")
	dotenv_stub.load_dotenv = lambda *args, **kwargs: None
	sys.modules["dotenv"] = dotenv_stub
