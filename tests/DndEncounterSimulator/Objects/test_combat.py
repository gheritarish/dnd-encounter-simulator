import json

import pytest

from DndEncounterSimulator.Objects.Combat import Combat
from DndEncounterSimulator.Objects.Creature import Monster
from DndEncounterSimulator.Objects.Weapon import Weapon
from DndEncounterSimulator.Tools.utils.Stats import STATS_GOBLIN, STATS_KENKU


@pytest.fixture()
def enemies_definition_test():
    with open("tests/DndEncounterSimulator/Objects/fixtures/enemies.json", "r") as f:
        standard_values_enemies = json.load(f)
    return standard_values_enemies


def test_combat_is_over_same_camp(enemies_definition_test):
    standard_values_enemies = enemies_definition_test
    scimitar = Weapon(name="scimitar", stat_to_hit="dexterity", damage="1d6")
    kenku = Monster(
        name=standard_values_enemies[0]["name"],
        armor_class=standard_values_enemies[0]["armor_class"],
        hit_points=standard_values_enemies[0]["hit_points"],
        weapons=[scimitar],
        stats=STATS_KENKU,
        proficiency=standard_values_enemies[0]["proficiency"],
        camp="red",
    )

    shortsword = Weapon(name="shortsword", stat_to_hit="dexterity", damage="1d6")
    goblin = Monster(
        name=standard_values_enemies[1]["name"],
        armor_class=standard_values_enemies[1]["armor_class"],
        hit_points=standard_values_enemies[1]["hit_points"],
        weapons=[shortsword],
        stats=STATS_GOBLIN,
        proficiency=standard_values_enemies[1]["proficiency"],
        camp="red",
    )

    test_combat = Combat(monsters=[kenku, goblin])
    test_is_over = test_combat.is_over()
    try:
        assert test_is_over
    except Exception as error:
        pytest.fail(f"Failed to compute if the fight is over. Error: {error}")


def test_combat_is_over_different_camp(enemies_definition_test):
    standard_values_enemies = enemies_definition_test
    scimitar = Weapon(name="scimitar", stat_to_hit="dexterity", damage="1d6")
    kenku = Monster(
        name=standard_values_enemies[0]["name"],
        armor_class=standard_values_enemies[0]["armor_class"],
        hit_points=standard_values_enemies[0]["hit_points"],
        weapons=[scimitar],
        stats=STATS_KENKU,
        proficiency=standard_values_enemies[0]["proficiency"],
        camp="red",
    )

    shortsword = Weapon(name="shortsword", stat_to_hit="dexterity", damage="1d6")
    goblin = Monster(
        name=standard_values_enemies[1]["name"],
        armor_class=standard_values_enemies[1]["armor_class"],
        hit_points=standard_values_enemies[1]["hit_points"],
        weapons=[shortsword],
        stats=STATS_GOBLIN,
        proficiency=standard_values_enemies[1]["proficiency"],
        camp="blue",
    )

    test_combat = Combat(monsters=[kenku, goblin])
    test_is_over = test_combat.is_over()
    try:
        assert not test_is_over
    except Exception as error:
        pytest.fail(f"Failed to compute if the fight is over. Error: {error}")
