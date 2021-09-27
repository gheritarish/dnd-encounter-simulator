import pytest

from DndEncounterSimulator.Objects.Weapon import Weapon


def test_critical_hit():
    weapon = Weapon(name="dummy", stat_to_hit="strength", damage="2d6")
    critical_damage = weapon.critical_hit()
    try:
        assert critical_damage == "4d6"
    except Exception as error:
        pytest.fail(f"Failed critical damage calculation. Error: {error}")
