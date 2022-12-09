from enum import Enum

from ansys.api.additive.v0.additive_domain_pb2 import (
    BEAD_TYPE_BEAD_ON_BASE_PLATE,
    BEAD_TYPE_BEAD_ON_POWDER_LAYER,
)
from ansys.api.additive.v0.additive_domain_pb2 import MeltPool as MeltPoolMessage
from ansys.api.additive.v0.additive_domain_pb2 import SingleBeadInput as SingleBeadInputMessage
from ansys.api.additive.v0.additive_simulation_pb2 import SimulationRequest

from ansys.additive.machine import AdditiveMachine
from ansys.additive.material import AdditiveMaterial


class BeadType(Enum):
    BEAD_ON_POWDER = BEAD_TYPE_BEAD_ON_POWDER_LAYER
    BEAD_ON_BASE_PLATE = BEAD_TYPE_BEAD_ON_BASE_PLATE


class SingleBeadInput:
    """Input parameters for single bead simulation

    Properties
    ----------

    id: string
        User provided identifier for this simulation
    machine: AdditiveMachine
        Machine related parameters
    material: AdditiveMaterial
        Material used during simulation
    bead_length: float
        Length of bead to simulate (m)
    bead_type: BeadType
        Type of bead, either BEAD_ON_POWDER or BEAD_ON_BASE_PLATE

    """

    def __init__(self, **kwargs):
        self.id = ""
        self.bead_length = 1e-3
        self.bead_type = BeadType.BEAD_ON_POWDER
        self.machine = AdditiveMachine()
        self.material = AdditiveMaterial()
        for key, value in kwargs.items():
            getattr(self, key)  # raises AttributeError if key not found
            setattr(self, key, value)

    def __repr__(self):
        repr = type(self).__name__ + "\n"
        for k in self.__dict__:
            if k == "machine" or k == "material":
                repr += "\n" + k + ": " + str(getattr(self, k))
            else:
                repr += k + ": " + str(getattr(self, k)) + "\n"
        return repr

    def to_simulation_request(self) -> SimulationRequest:
        """Convert this object into a simulation request message"""
        input = SingleBeadInputMessage(
            machine=self.machine.to_machine_message(),
            material=self.material.to_material_message(),
            bead_length=self.bead_length,
        )
        if self.bead_type == BeadType.BEAD_ON_BASE_PLATE:
            input.bead_type = BEAD_TYPE_BEAD_ON_BASE_PLATE
        else:
            input.bead_type = BEAD_TYPE_BEAD_ON_POWDER_LAYER
        return SimulationRequest(id=self.id, single_bead_input=input)


class MeltPool:
    """Description of the melt pool evolution during a single bead simulation

    Each index in the property arrays represents a single time step

    Units are SI unless otherwise noted.

    Properties
    ----------

    laser_x: float[]
        Laser position x coordinate.
    laser_y: float[]
        Laser position y coordinate.
    length: float[]
        Melt pool length at surface.
    width: float[]
        Current melt pool width at surface.
    depth: float[]
        Melt pool depth from surface.
    reference_width: float[]
        Melt pool width at the bottom of the powder layer, or width at top
        of substrate.
    reference_depth: float[]
        Depth of the entire melt pool minus the powder layer thickness, or
        depth of penetration into substrate.

    """

    def __init__(self, melt_pool: MeltPoolMessage):
        self._laser_x = []
        self._laser_y = []
        self._length = []
        self._width = []
        self._depth = []
        self._reference_width = []
        self._reference_depth = []

        for ts in melt_pool.time_steps:
            self._laser_x.append(ts.laser_x)
            self._laser_y.append(ts.laser_y)
            self._length.append(ts.length)
            self._width.append(ts.width)
            self._depth.append(ts.depth)
            self._reference_width.append(ts.reference_width)
            self._reference_depth.append(ts.reference_depth)

    @property
    def laser_x(self):
        return self._laser_x

    @property
    def laser_y(self):
        return self._laser_y

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def reference_width(self):
        return self._reference_width

    @property
    def reference_depth(self):
        return self._reference_depth

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, MeltPool):
            return False
        for k in self.__dict__:
            if getattr(self, k) != getattr(__o, k):
                return False
        return True

    def __repr__(self):
        repr = type(self).__name__ + "\n"
        for k in self.__dict__:
            repr += k.replace("_", "", 1) + ": " + str(getattr(self, k)) + "\n"
        return repr


class SingleBeadSummary:
    """Summary of a single bead simulation

    Units are SI unless otherwise noted.

    Properties
    ----------

    input: SingleBeadInput
        Simulation input parameters
    msg: MeltPoolMessage
        Melt pool evolution message received from server

    """

    def __init__(
        self,
        input: SingleBeadInput,
        msg: MeltPoolMessage,
    ):
        if not isinstance(input, SingleBeadInput):
            raise ValueError("Invalid input type passed to init, " + self.__class__.__name__)
        if not isinstance(msg, MeltPoolMessage):
            raise ValueError("Invalid message type passed to init, " + self.__class__.__name__)
        self._input = input
        self._melt_pool = MeltPool(msg)

    @property
    def input(self):
        return self._input

    @property
    def melt_pool(self):
        return self._melt_pool

    def __repr__(self):
        repr = type(self).__name__ + "\n"
        for k in self.__dict__:
            repr += k.replace("_", "", 1) + ": " + str(getattr(self, k)) + "\n"
        return repr
