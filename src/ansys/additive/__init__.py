# (c) 2023 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
"""PyAdditive is a Python client for the Ansys Additive service."""
import os

import platformdirs

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

APP_NAME = "ansys-pyadditive"
COMPANY_NAME = "Ansys Inc"


# Setup data directory
USER_DATA_PATH = platformdirs.user_data_dir(APP_NAME, COMPANY_NAME)
if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
    os.makedirs(USER_DATA_PATH)

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
    os.makedirs(EXAMPLES_PATH)

from ansys.additive.additive import (
    DEFAULT_ADDITIVE_SERVICE_PORT,
    LOCALHOST,
    MAX_MESSAGE_LENGTH,
    Additive,
)
from ansys.additive.geometry_file import BuildFile, MachineType, StlFile
from ansys.additive.machine import AdditiveMachine, MachineConstants
from ansys.additive.material import (
    AdditiveMaterial,
    CharacteristicWidthDataPoint,
    ThermalPropertiesDataPoint,
)
from ansys.additive.material_tuning import MaterialTuningInput, MaterialTuningSummary
from ansys.additive.microstructure import (
    CircleEquivalenceColumnNames,
    MicrostructureInput,
    MicrostructureSummary,
)
from ansys.additive.porosity import PorosityInput, PorositySummary
from ansys.additive.server_utils import find_open_port, launch_server
from ansys.additive.simulation import SimulationError, SimulationStatus, SimulationType
from ansys.additive.single_bead import (
    MeltPool,
    MeltPoolColumnNames,
    SingleBeadInput,
    SingleBeadSummary,
)
from ansys.additive.thermal_history import (
    CoaxialAverageSensorInputs,
    Range,
    ThermalHistoryInput,
    ThermalHistorySummary,
)
