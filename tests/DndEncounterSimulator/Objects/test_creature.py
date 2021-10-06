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
        type_of_damage="slashing",
    )
    shortsword = Weapon(
        name=standard_weapons[1]["name"],
        stat_to_hit=standard_weapons[1]["stat_to_hit"],
        damage=standard_weapons[1]["damage"],
        type_of_damage="slashing",
    )
    longsword = Weapon(
        name=standard_weapons[2]["name"],
        stat_to_hit=standard_weapons[2]["stat_to_hit"],
        damage=standard_weapons[2]["damage"],
        type_of_damage="slashing",
    )
    falchion = Weapon(
        name=standard_weapons[3]["name"],
        stat_to_hit=standard_weapons[3]["stat_to_hit"],
        damage=standard_weapons[3]["damage"],
        type_of_damage="slashing",
    )
    kenku = Monster(
        name="kenku",
        armor_class=13,
        hit_points=13,
        proficiency=2,
        stats=STATS_KENKU,
        weapons=[scimitar, shortsword, longsword, falchion],
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
    kenku.change_weapon(5)  # outside range: no change should be made
    try:
        assert kenku.weapons[0].name == "scimitar"
    except Exception as error:
        pytest.fail(f"Failed to prevent weapon change outside range. Error: {error}")
