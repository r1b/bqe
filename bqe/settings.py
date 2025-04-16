import os
from pathlib import Path

BQE_DEBUG = bool(os.environ.get("BQE_DEBUG"))
PACKAGE_ROOT = Path(__file__).parent
