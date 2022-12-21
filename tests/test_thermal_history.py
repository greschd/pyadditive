from ansys.api.additive.v0.additive_domain_pb2 import BuildFileMachineType
from ansys.api.additive.v0.additive_domain_pb2 import StlFile as StlFileMessage
from ansys.api.additive.v0.additive_domain_pb2 import ThermalHistoryResult
from ansys.api.additive.v0.additive_simulation_pb2 import SimulationRequest
import pytest

from ansys.additive.geometry_file import BuildFile, MachineType, StlFile
from ansys.additive.machine import AdditiveMachine
from ansys.additive.material import AdditiveMaterial
from ansys.additive.thermal_history import (
    CoaxialAverageSensorInputs,
    CoaxialAverageSensorInputsMessage,
    Range,
    RangeMessage,
    ThermalHistoryInput,
    ThermalHistoryInputMessage,
    ThermalHistorySummary,
)


def test_Range_init_returns_expected_value():
    # arrange, act
    range = Range()

    # assert
    assert isinstance(range, Range)
    assert range.min == 0 and range.max == 0


def test_Range_init_with_parameters_returns_expected_value():
    # arrange, act
    range = Range(min=99, max=100)

    # assert
    assert isinstance(range, Range)
    assert range.min == 99 and range.max == 100


def test_Range_init_raises_exception_for_invalid_input():
    # arrange, act, assert
    with pytest.raises(AttributeError, match="'Range' object has no attribute 'bogus'") as exc_info:
        Range(bogus=7)


def test_Range_init_raises_exception_for_min_greater_than_max():
    # arrange, act, assert
    with pytest.raises(
        ValueError, match="Attempted to initialize Range with min greater than max"
    ) as exc_info:
        Range(min=100, max=99)


def test_Range_eq():
    # arrange
    range = Range()
    not_range = Range(min=-1)

    # act, assert
    assert range == Range()
    assert range != RangeMessage(min=0, max=0)
    assert range != not_range


def test_Range_repr():
    # arrange
    range = Range(min=2, max=3)

    # act, assert
    assert range.__repr__() == "Range\nmin: 2\nmax: 3\n"


def test_Range_to_range_message():
    # arrange
    range = Range(min=10, max=99)

    # act
    msg = range.to_range_message()

    # assert
    assert isinstance(msg, RangeMessage)
    assert msg.min == 10
    assert msg.max == 99


def test_CoaxialAverageSensorInputs_init_returns_expected_value():
    # arrange, act
    inputs = CoaxialAverageSensorInputs()

    # assert
    assert isinstance(inputs, CoaxialAverageSensorInputs)
    assert inputs.radius == 0
    assert inputs.z_heights == []


def test_CoaxialAverageSensorInputs_init_with_parameters_returns_expected_value():
    # arrange, act
    z_heights = [Range(min=1, max=2), Range(min=3, max=4)]
    inputs = CoaxialAverageSensorInputs(radius=1, z_heights=z_heights)

    # assert
    assert isinstance(inputs, CoaxialAverageSensorInputs)
    assert inputs.radius == 1
    assert inputs.z_heights == [Range(min=1, max=2), Range(min=3, max=4)]


def test_CoaxialAverageSensorInputs_init_raises_exception_for_invalid_input():
    # arrange, act, assert
    with pytest.raises(
        AttributeError, match="'CoaxialAverageSensorInputs' object has no attribute 'bogus'"
    ) as exc_info:
        CoaxialAverageSensorInputs(bogus=7)


def test_CoaxialAverageSensorInputs_init_raises_exception_for_radius_less_than_zero():
    # arrange, act, assert
    with pytest.raises(
        ValueError,
        match="Attempted to initialize CoaxialAverageSensorInputs with negative sensor radius",
    ) as exc_info:
        CoaxialAverageSensorInputs(radius=-1)


def test_CoaxialAverageSensorInputs_eq():
    # arrange
    inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    not_inputs = CoaxialAverageSensorInputs()

    # act, assert
    assert inputs == CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    assert inputs != CoaxialAverageSensorInputsMessage(
        sensor_radius=1, z_heights=[RangeMessage(min=1, max=2), RangeMessage(min=3, max=4)]
    )
    assert inputs != not_inputs


def test_CoaxialAverageSensorInputs_repr():
    # arrange
    inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )

    # act, assert
    assert (
        inputs.__repr__()
        == "CoaxialAverageSensorInputs\nradius: 1\nz_heights: "
        + "[Range\nmin: 1\nmax: 2\n, Range\nmin: 3\nmax: 4\n]\n"
    )


def test_CoaxialAverageSensorInputs_coaxial_average_sensor_inputs_message():
    # arrange
    inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    # act
    msg = inputs.to_coaxial_average_sensor_inputs_message()

    # assert
    assert isinstance(msg, CoaxialAverageSensorInputsMessage)
    assert msg.sensor_radius == 1
    assert len(msg.z_heights) == 2
    assert msg.z_heights[0] == RangeMessage(min=1, max=2)
    assert msg.z_heights[1] == RangeMessage(min=3, max=4)


def test_ThermalHistoryInput_init_creates_default_object():
    # arrange, act
    input = ThermalHistoryInput()

    # assert
    assert input.id == ""
    assert input.machine.laser_power == 195
    assert input.material.name == ""
    assert input.geometry == None
    assert input.coax_ave_sensor_inputs == CoaxialAverageSensorInputs()


def test_ThermalHistoryInput_init_with_parameters_creates_expected_object():
    # arrange
    machine = AdditiveMachine()
    machine.laser_power = 99
    material = AdditiveMaterial(name="vibranium")
    coax_inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    stl_file = StlFile(path="geometry.stl")

    # act
    input = ThermalHistoryInput(
        id="myId",
        machine=machine,
        material=material,
        coax_ave_sensor_inputs=coax_inputs,
        geometry=stl_file,
    )

    # assert
    assert "myId" == input.id
    assert input.machine.laser_power == 99
    assert input.material.name == "vibranium"
    assert input.coax_ave_sensor_inputs == coax_inputs
    assert input.geometry == stl_file


def test_ThermalHistoryInput_init_raises_exception_for_invalid_input():
    # arrange, act, assert
    with pytest.raises(AttributeError):
        ThermalHistoryInput(bogus="invalid")


def test_ThermalHistoryInput_repr_creates_expected_string():
    # arrange
    coax_inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    stl_file = StlFile(path="geometry.stl")

    # act
    input = ThermalHistoryInput(
        id="myId",
        machine=AdditiveMachine(),
        material=AdditiveMaterial(),
        coax_ave_sensor_inputs=coax_inputs,
        geometry=stl_file,
    )

    # assert
    assert (
        input.__repr__()
        == "ThermalHistoryInput\n"
        + "id: myId\n"
        + "geometry: StlFile\n"
        + "path: geometry.stl\n"
        + "\n"
        + "coax_ave_sensor_inputs: CoaxialAverageSensorInputs\n"
        + "radius: 1\n"
        + "z_heights: [Range\n"
        + "min: 1\n"
        + "max: 2\n"
        + ", Range\n"
        + "min: 3\n"
        + "max: 4\n"
        + "]\n"
        + "\n"
        + "\n"
        + "machine: AdditiveMachine\n"
        + "laser_power: 195\n"
        + "scan_speed: 1.0\n"
        + "heater_temperature: 80\n"
        + "layer_thickness: 5e-05\n"
        + "beam_diameter: 0.0001\n"
        + "starting_layer_angle: 57\n"
        + "layer_rotation_angle: 67\n"
        + "hatch_spacing: 0.0001\n"
        + "slicing_stripe_width: 0.01\n"
        + "\n"
        + "material: AdditiveMaterial\n"
        + "absorptivity_maximum: 0\n"
        + "absorptivity_minimum: 0\n"
        + "absorptivity_powder_coefficient_a: 0\n"
        + "absorptivity_powder_coefficient_b: 0\n"
        + "absorptivity_solid_coefficient_a: 0\n"
        + "absorptivity_solid_coefficient_b: 0\n"
        + "anisotropic_strain_coefficient_parallel: 0\n"
        + "anisotropic_strain_coefficient_perpendicular: 0\n"
        + "anisotropic_strain_coefficient_z: 0\n"
        + "elastic_modulus: 0\n"
        + "hardening_factor: 0\n"
        + "liquidus_temperature: 0\n"
        + "material_yield_strength: 0\n"
        + "name: \n"
        + "nucleation_constant_bulk: 0\n"
        + "nucleation_constant_interface: 0\n"
        + "penetration_depth_maximum: 0\n"
        + "penetration_depth_minimum: 0\n"
        + "penetration_depth_powder_coefficient_a: 0\n"
        + "penetration_depth_powder_coefficient_b: 0\n"
        + "penetration_depth_solid_coefficient_a: 0\n"
        + "penetration_depth_solid_coefficient_b: 0\n"
        + "poisson_ratio: 0\n"
        + "powder_packing_density: 0\n"
        + "purging_gas_convection_coefficient: 0\n"
        + "solid_density_at_room_temperature: 0\n"
        + "solid_specific_heat_at_room_temperature: 0\n"
        + "solid_thermal_conductivity_at_room_temperature: 0\n"
        + "solidus_temperature: 0\n"
        + "strain_scaling_factor: 0\n"
        + "support_yield_strength_ratio: 0\n"
        + "thermal_expansion_coefficient: 0\n"
        + "vaporization_temperature: 0\n"
        + "characteristic_width_data: CharacteristicWidthDataPoint[]\n"
        + "thermal_characteristic_data: ThermalCharacteristicDataPoint[]\n"
    )


def test_ThermalHistoryInput_eq():
    # arrange
    machine = AdditiveMachine()
    machine.laser_power = 99
    material = AdditiveMaterial(name="vibranium")
    coax_inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    stl_file = StlFile(path="geometry.stl")

    # act
    input = ThermalHistoryInput(
        id="myId",
        machine=machine,
        material=material,
        coax_ave_sensor_inputs=coax_inputs,
        geometry=stl_file,
    )
    input2 = ThermalHistoryInput(machine=machine, material=material)

    # act, assert
    assert input == ThermalHistoryInput(
        id="myId",
        machine=machine,
        material=material,
        coax_ave_sensor_inputs=coax_inputs,
        geometry=stl_file,
    )
    assert input != ThermalHistoryInput()
    assert input != ThermalHistoryInputMessage(
        machine=machine.to_machine_message(),
        material=material.to_material_message(),
        coax_ave_sensor_inputs=coax_inputs.to_coaxial_average_sensor_inputs_message(),
        stl_file=StlFileMessage(name=stl_file.path),
    )
    assert input2 != ThermalHistoryInput()
    assert input != input2


def test_ThermalHistoryInput_geometry_setter_raises_exception_for_bad_input():
    # arrange
    input = ThermalHistoryInput()

    # act, assert
    with pytest.raises(TypeError):
        input.geometry = "my_geometry.stl"


def test_ThermalHistoryInput_to_simulation_request_with_stl_file_returns_expected_object():
    # arrange
    remote_path = "remote.stl"
    machine = AdditiveMachine()
    machine.laser_power = 99
    material = AdditiveMaterial(name="vibranium")
    coax_inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    stl_file = StlFile(path="geometry.stl")
    input = ThermalHistoryInput(
        id="myId",
        machine=machine,
        material=material,
        coax_ave_sensor_inputs=coax_inputs,
        geometry=stl_file,
    )

    # act
    request = input.to_simulation_request(remote_path)

    # assert
    assert isinstance(request, SimulationRequest)
    assert request.id == "myId"
    th_input = request.thermal_history_input
    assert th_input.stl_file != None
    assert remote_path == th_input.stl_file.name
    assert coax_inputs.to_coaxial_average_sensor_inputs_message() == th_input.coax_ave_sensor_inputs
    assert machine.laser_power == th_input.machine.laser_power
    assert material.name == th_input.material.name


# TODO: Change this to use build file
def test_ThermalHistoryInput_to_simulation_request_assigns_values():
    # arrange
    remote_path = "remote-file.zip"
    machine = AdditiveMachine()
    machine.laser_power = 99
    material = AdditiveMaterial(name="vibranium")
    coax_inputs = CoaxialAverageSensorInputs(
        radius=1, z_heights=[Range(min=1, max=2), Range(min=3, max=4)]
    )
    build_file = BuildFile(type=MachineType.EOS, path="build.zip")
    input = ThermalHistoryInput(
        id="myId",
        machine=machine,
        material=material,
        coax_ave_sensor_inputs=coax_inputs,
        geometry=build_file,
    )

    # act
    request = input.to_simulation_request(remote_path)

    # assert
    assert isinstance(request, SimulationRequest)
    assert request.id == "myId"
    th_input = request.thermal_history_input
    assert th_input.build_file != None
    assert remote_path == th_input.build_file.name
    assert BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_EOS == th_input.build_file.type
    assert coax_inputs.to_coaxial_average_sensor_inputs_message() == th_input.coax_ave_sensor_inputs
    assert machine.laser_power == th_input.machine.laser_power
    assert material.name == th_input.material.name


def test_ThermalHistoryInput_to_simulation_request_raises_exception_when_geometry_not_defined():
    input = ThermalHistoryInput()
    # act, assert
    with pytest.raises(
        ValueError, match="Attempted to create simulation request without defining geometry"
    ) as exc_info:
        input.to_simulation_request("remote_path")


def test_ThermalHistoryInput_to_simulation_request_raises_exception_when_remote_path_not_defined():
    input = ThermalHistoryInput(geometry=StlFile(path="my.stl"))
    # act, assert
    with pytest.raises(
        ValueError, match="Attempted to create simulation request with empty remote_geometry_path"
    ) as exc_info:
        input.to_simulation_request("")


def test_ThermalHistorySummary_init_returns_expected_value():
    # arrange
    input = ThermalHistoryInput()
    result = ThermalHistoryResult(coax_ave_zip_file="coax_file.zip")

    # act
    summary = ThermalHistorySummary(input, result)

    # assert
    assert isinstance(summary, ThermalHistorySummary)
    assert input == summary.input
    assert summary.remote_coax_ave_zip_file == "coax_file.zip"


@pytest.mark.parametrize(
    "invalid_obj",
    [
        int(1),
        None,
        ThermalHistoryResult(),
    ],
)
def test_ThermalHistorySummary_init_raises_exception_for_invalid_input_type(
    invalid_obj,
):
    # arrange, act, assert
    with pytest.raises(ValueError, match="Invalid input type") as exc_info:
        ThermalHistorySummary(invalid_obj, ThermalHistoryResult())


@pytest.mark.parametrize(
    "invalid_obj",
    [
        int(1),
        None,
        ThermalHistoryInput(),
    ],
)
def test_ThermalHistorySummary_init_raises_exception_for_invalid_result_type(
    invalid_obj,
):
    # arrange, act, assert
    with pytest.raises(ValueError, match="Invalid result type") as exc_info:
        ThermalHistorySummary(ThermalHistoryInput(), invalid_obj)