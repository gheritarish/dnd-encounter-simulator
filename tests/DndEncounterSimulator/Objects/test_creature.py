import json

import pytest

from DndEncounterSimulator.Objects.Creature import Monster
from DndEncounterSimulator.Objects.Weapon import Weapon
from DndEncounterSimulator.Tools.utils.Stats import STATS_KENKU


@pytest.fixture()
def weapons_definition_test():
    with open("tests/DndEncounterSimulator/Objects/fixtures/weapons.json", "r") as f:
        standard_weapons = json.load(f)
    return standard_weapons


@pytest.fixture()
def create_kenku_w_weapons(weapons_definition_test):
    standard_weapons = weapons_definition_test
    scimitar = Weapon(
        name=standard_weapons[0]["name"],
        stat_to_hit=standard_weapons[0]["stat_to_hit"],
        damage=standard_weapons[0]["damage"],
        type_of_damage=standard_weapons[0]["type_of_damage"],
    )
    shortsword = Weapon(
        name=standard_weapons[1]["name"],
        stat_to_hit=standard_weapons[1]["stat_to_hit"],
        damage=standard_weapons[1]["damage"],
        type_of_damage=standard_weapons[1]["type_of_damage"],
    )
    longsword = Weapon(
        name=standard_weapons[2]["name"],
        stat_to_hit=standard_weapons[2]["stat_to_hit"],
        damage=standard_weapons[2]["damage"],
        type_of_damage=standard_weapons[2]["type_of_damage"],
    )
    falchion = Weapon(
        name=standard_weapons[3]["name"],
        stat_to_hit=standard_weapons[3]["stat_to_hit"],
        damage=standard_weapons[3]["damage"],
        type_of_damage=standard_weapons[3]["type_of_damage"],
    )
    quarterstaff = Weapon(
        name=standard_weapons[4]["name"],
        stat_to_hit=standard_weapons[4]["stat_to_hit"],
        damage=standard_weapons[4]["damage"],
        type_of_damage=standard_weapons[4]["type_of_damage"],
    )
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[scimitar, shortsword, longsword, falchion, quarterstaff],
        resistances=[],
        immunities=[],
        vulnerabilities=[],
        camp="red",
    )
    return kenku


def test_find_best_weapon(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    best_weapon_index = kenku.find_best_weapon()
    try:
        assert best_weapon_index == 3
    except Exception as error:
        pytest.fail(f"Failed to find best weapon. Error: {error}")


def test_to_find_best_weapon_without_weapon():
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[],
        resistances=[],
        immunities=[],
        vulnerabilities=[],
        camp="red",
    )
    with pytest.raises(IndexError):
        assert kenku.find_best_weapon(
            known_resistances=[], known_immunities=[], known_vulnerabilities=[]
        )


def test_change_weapon(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    kenku.change_weapon(2)  # we want the longsword
    try:
        assert kenku.weapons[0].name == "longsword"
    except Exception as error:
        pytest.fail(f"Failed to change weapon. Error: {error}")


def test_change_weapon_outside_range(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    kenku.change_weapon(6)  # outside range: no change should be made
    try:
        assert kenku.weapons[0].name == "scimitar"
    except Exception as error:
        pytest.fail(f"Failed to prevent weapon change outside range. Error: {error}")


def test_choose_weapon_with_vulnerability(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    best_weapon_index = kenku.find_best_weapon(known_vulnerabilities=["bludgeoning"])
    try:
        assert best_weapon_index == 4  # With vulnerability, best weapon is the staff
    except Exception as error:
        pytest.fail(f"Failed to find best weapon with vulnerability. Error: {error}")


def test_choose_weapon_with_resistance(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    best_weapon_index = kenku.find_best_weapon(known_resistances=["slashing"])
    try:
        assert best_weapon_index == 4  # With resistance, best weapon is the staff
    except Exception as error:
        pytest.fail(f"Failed to find best weapon with resistance. Error: {error}")


def test_choose_weapon_with_immunity(create_kenku_w_weapons):
    kenku = create_kenku_w_weapons
    best_weapon_index = kenku.find_best_weapon(known_immunities=["slashing"])
    try:
        assert best_weapon_index == 4  # With immunity, best weapon is the staff
    except Exception as error:
        pytest.fail(f"Failed to find best weapon with immunity. Error: {error}")


def test_damage_with_resistance():
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[],
        resistances=["bludgeoning"],
        immunities=[],
        vulnerabilities=[],
        camp="red",
    )
    kenku.damage(5, "bludgeoning")
    try:
        kenku.hit_points == 11  # Resistance divides 5 by 2, rounded down
    except Exception as error:
        pytest.fail(f"Failed to take resistance into account. Error: {error}")


def test_damage_with_immunity():
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[],
        resistances=[],
        immunities=["bludgeoning"],
        vulnerabilities=[],
        camp="red",
    )
    kenku.damage(5, "bludgeoning")
    try:
        kenku.hit_points == 13  # With immunity, no damage taken
    except Exception as error:
        pytest.fail(f"Failed to take immunity into account. Error: {error}")


def test_damage_with_vulnerability():
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[],
        resistances=[],
        immunities=[],
        vulnerabilities=["bludgeoning"],
        camp="red",
    )
    kenku.damage(5, "bludgeoning")
    try:
        kenku.hit_points == 3  # Vulnerability doubles the damages
    except Exception as error:
        pytest.fail(f"Failed to take resistance into account. Error: {error}")
