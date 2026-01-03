import os

from dotenv import load_dotenv

load_dotenv()
class EnvConfig:
    OUTPUT_STL_DIR_PATH = os.environ["OUTPUT_STL_DIR_PATH"]
