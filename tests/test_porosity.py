# (c) 2023 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
from ansys.api.additive.v0.additive_domain_pb2 import PorosityResult
from ansys.api.additive.v0.additive_simulation_pb2 import SimulationRequest
import pytest

from ansys.additive.core.machine import AdditiveMachine
from ansys.additive.core.material import AdditiveMaterial
from ansys.additive.core.porosity import PorosityInput, PorositySummary

from . import test_utils


def test_PorosityInput_init_creates_default_object():
    # arrange, act
    machine = AdditiveMachine()
    material = AdditiveMaterial()
    input = PorosityInput()

    # assert
    assert "" == input.id
    assert 3e-3 == input.size_x
    assert 3e-3 == input.size_y
    assert 3e-3 == input.size_z
    assert machine == input.machine
    assert material == input.material


def test_PorosityInput_init_creates_expected_object():
    # arrange, act
    machine = AdditiveMachine(laser_power=100)
    material = test_utils.get_test_material()
    input = PorosityInput(
        id="id",
        size_x=1e-3,
        size_y=2e-3,
        size_z=3e-3,
        machine=machine,
        material=material,
    )

    # assert
    assert "id" == input.id
    assert 1e-3 == input.size_x
    assert 2e-3 == input.size_y
    assert 3e-3 == input.size_z
    assert machine == input.machine
    assert material == input.material


def test_PorositySummary_init_creates_expected_object():
    # arrange
    input = PorosityInput(
        id="id",
        size_x=1e-3,
        size_y=2e-3,
        size_z=3e-3,
        machine=AdditiveMachine(),
        material=test_utils.get_test_material(),
    )

    result = PorosityResult(
        void_ratio=10,
        powder_ratio=11,
        solid_ratio=12,
    )

    # act
    summary = PorositySummary(input, result)

    # assert
    assert input == summary.input
    assert 12 == summary.relative_density


@pytest.mark.parametrize(
    "invalid_obj",
    [
        int(1),
        None,
        PorosityResult(),
    ],
)
def test_PorositySummary_init_raises_exception_for_invalid_input_type(invalid_obj):
    # arrange, act, assert
    with pytest.raises(ValueError, match="Invalid input type") as exc_info:
        PorositySummary(invalid_obj, PorosityResult())


@pytest.mark.parametrize(
    "invalid_obj",
    [
        int(1),
        None,
        PorosityInput(),
    ],
)
def test_PorositySummary_init_raises_exception_for_invalid_result_type(invalid_obj):
    # arrange, act, assert
    with pytest.raises(ValueError, match="Invalid result type") as exc_info:
        PorositySummary(PorosityInput(), invalid_obj)


def test_PorosityInput__to_simulation_request_assigns_values():
    # arrange
    machine = AdditiveMachine()
    machine.laser_power = 99
    material = AdditiveMaterial(name="vibranium")
    input = PorosityInput(
        id="myId", machine=machine, material=material, size_x=1e-3, size_y=2e-3, size_z=3e-3
    )

    # act
    request = input._to_simulation_request()

    # assert
    assert isinstance(request, SimulationRequest)
    assert request.id == "myId"
    p_input = request.porosity_input
    assert p_input.machine.laser_power == 99
    assert p_input.material.name == "vibranium"
    assert p_input.size_x == 1e-3
    assert p_input.size_y == 2e-3
    assert p_input.size_z == 3e-3


def test_PorosityInput_setters_raise_expected_errors():
    # arrange
    input = PorosityInput()

    # act, assert
    with pytest.raises(ValueError):
        input.size_x = 0.9e-3
    with pytest.raises(ValueError):
        input.size_x = 1.1e-2
    with pytest.raises(ValueError):
        input.size_y = 0.9e-3
    with pytest.raises(ValueError):
        input.size_y = 1.1e-2
    with pytest.raises(ValueError):
        input.size_z = 0.9e-3
    with pytest.raises(ValueError):
        input.size_z = 1.1e-2


def test_PorosityInput_repr_returns_expected_string():
    # arrange
    input = PorosityInput(id="myId")

    # act, assert
    assert repr(input) == (
        "PorosityInput\n"
        + "id: myId\n"
        + "size_x: 0.003\n"
        + "size_y: 0.003\n"
        + "size_z: 0.003\n"
        + "\n"
        + "machine: AdditiveMachine\n"
        + "laser_power: 195 W\n"
        + "scan_speed: 1.0 m/s\n"
        + "heater_temperature: 80 °C\n"
        + "layer_thickness: 5e-05 m\n"
        + "beam_diameter: 0.0001 m\n"
        + "starting_layer_angle: 57 °\n"
        + "layer_rotation_angle: 67 °\n"
        + "hatch_spacing: 0.0001 m\n"
        + "slicing_stripe_width: 0.01 m\n"
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
        + "thermal_properties_data: ThermalPropertiesDataPoint[]\n"
    )


def test_PorositySummary_repr_retuns_expected_string():
    # arrange
    input = PorosityInput(id="myId")
    result = PorosityResult()
    summary = PorositySummary(input, result)

    # act, assert
    assert repr(summary) == (
        "PorositySummary\n"
        + "input: PorosityInput\n"
        + "id: myId\n"
        + "size_x: 0.003\n"
        + "size_y: 0.003\n"
        + "size_z: 0.003\n"
        + "\n"
        + "machine: AdditiveMachine\n"
        + "laser_power: 195 W\n"
        + "scan_speed: 1.0 m/s\n"
        + "heater_temperature: 80 °C\n"
        + "layer_thickness: 5e-05 m\n"
        + "beam_diameter: 0.0001 m\n"
        + "starting_layer_angle: 57 °\n"
        + "layer_rotation_angle: 67 °\n"
        + "hatch_spacing: 0.0001 m\n"
        + "slicing_stripe_width: 0.01 m\n"
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
        + "thermal_properties_data: ThermalPropertiesDataPoint[]\n"
        + "\n"
        + "relative_density: 0.0\n"
    )
