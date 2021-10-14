import pytest

from DndEncounterSimulator.Objects.Weapon import DamageType, Weapon


def test_critical_hit():
    weapon = Weapon(
        name="dummy",
        stat_to_hit="strength",
        damage="2d6",
        type_of_damage=DamageType("bludgeoning"),
    )
    critical_damage = weapon.critical_hit()
    try:
        assert critical_damage == "4d6"
    except Exception as error:
        pytest.fail(f"Failed critical damage calculation. Error: {error}")


def test_average_damage_of_greatsword():
    weapon = Weapon(
        name="greatsword",
        stat_to_hit="strength",
        damage="2d6",
        type_of_damage=DamageType("slashing"),
    )
    mean_damage = weapon.average_damage()
    try:
        assert mean_damage == 7
    except Exception as error:
        pytest.fail(f"Failed to compute mean damages of a greatsword. Error: {error}")


def test_average_damage_of_shortsword():
    weapon = Weapon(
        name="shortsword",
        stat_to_hit="dexterity",
        damage="1d6",
        type_of_damage=DamageType("slashing"),
    )
    mean_damage = weapon.average_damage()
    try:
        assert mean_damage == 3.5
    except Exception as error:
        pytest.fail(f"Failed to compute mean damage of a shortsword. Error: {error}")
