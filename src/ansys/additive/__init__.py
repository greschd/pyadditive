# (c) 2023 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
"""
PyAdditive is a Python client for the Ansys additive service.
"""
import os

import appdirs

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

APP_NAME = "ansys-pyadditive"
COMPANY_NAME = "Ansys Inc"


# Setup data directory
# try:
USER_DATA_PATH = appdirs.user_data_dir(APP_NAME, COMPANY_NAME)
if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
    os.makedirs(USER_DATA_PATH)

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
    os.makedirs(EXAMPLES_PATH)

# except:  # pragma: no cover
#     pass

from .additive import *
from .geometry_file import *
from .machine import *
from .material import *
from .material_tuning import *
from .microstructure import *
from .porosity import *
from .server_utils import *
from .single_bead import *
from .thermal_history import *
