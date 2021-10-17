import json

import pytest

from DndEncounterSimulator.Objects.Combat import Combat
from DndEncounterSimulator.Objects.Creature import Monster
from DndEncounterSimulator.Objects.Weapon import DamageType, Weapon
from DndEncounterSimulator.Tools.utils.Stats import STATS_GOBLIN, STATS_KENKU


@pytest.fixture()
def enemies_definition_test():
    with open("tests/DndEncounterSimulator/Objects/fixtures/enemies.json", "r") as f:
        standard_values_enemies = json.load(f)
    return standard_values_enemies


@pytest.fixture()
def create_scimitar_test():
    scimitar = Weapon(
        name="scimitar",
        stat_to_hit="dexterity",
        damage="1d6",
        type_of_damage=DamageType("slashing"),
    )
    return scimitar


@pytest.fixture()
def create_shortsword_test():
    shortsword = Weapon(
        name="shortsword",
        stat_to_hit="dexterity",
        damage="1d6",
        type_of_damage=DamageType("slashing"),
    )
    return shortsword


@pytest.fixture()
def create_kenku_test(enemies_definition_test, create_scimitar_test):
    standard_values_enemies = enemies_definition_test
    scimitar = create_scimitar_test
    kenku = Monster(
        name=standard_values_enemies[0]["name"],
        armor_class=standard_values_enemies[0]["armor_class"],
        hit_points=standard_values_enemies[0]["hit_points"],
        weapons=[scimitar],
        stats=STATS_KENKU,
        proficiency=standard_values_enemies[0]["proficiency"],
        resistances=[],
        immunities=[],
        vulnerabilities=[],
        camp="blue",
    )
    return kenku


@pytest.fixture()
def create_goblin_test(enemies_definition_test, create_shortsword_test):
    standard_values_enemies = enemies_definition_test
    shortsword = create_shortsword_test
    goblin = Monster(
        name=standard_values_enemies[1]["name"],
        armor_class=standard_values_enemies[1]["armor_class"],
        hit_points=standard_values_enemies[1]["hit_points"],
        weapons=[shortsword],
        stats=STATS_GOBLIN,
        proficiency=standard_values_enemies[1]["proficiency"],
        resistances=[],
        immunities=[],
        vulnerabilities=[],
        camp="red",
    )
    return goblin


def test_combat_is_over_same_camp(create_goblin_test):
    goblin = create_goblin_test
    test_combat = Combat(monsters=[goblin, goblin])
    test_is_over = test_combat.is_over()
    try:
        assert test_is_over
    except Exception as error:
        pytest.fail(f"Failed to compute if the fight is over. Error: {error}")


def test_combat_is_over_different_camp(create_kenku_test, create_goblin_test):
    kenku = create_kenku_test
    goblin = create_goblin_test

    test_combat = Combat(monsters=[kenku, goblin])
    test_is_over = test_combat.is_over()
    try:
        assert not test_is_over
    except Exception as error:
        pytest.fail(f"Failed to compute if the fight is over. Error: {error}")


def test_find_wounded_opponent_in_enemy_camp_index_0(
    create_kenku_test, create_goblin_test
):
    kenku = create_kenku_test
    goblin = create_goblin_test
    test_combat = Combat(monsters=[kenku, kenku, goblin, goblin, goblin])
    test_wounded_creature = test_combat.fighters[0]
    test_combat.wounded_fighters[0] = True

    index = 0
    while test_combat.fighters[index].name == test_wounded_creature.name:
        index += 1
    test_opponent = test_combat.fighters[index].find_opponent(
        fighters=test_combat.fighters, wounded_fighters=test_combat.wounded_fighters
    )
    try:
        assert test_opponent == 0
    except Exception as error:
        pytest.fail(f"Failed to find the wounded opponent. Error: {error}")


def test_find_wounded_opponent_in_enemy_camp_index_2(
    create_kenku_test, create_goblin_test
):
    kenku = create_kenku_test
    goblin = create_goblin_test
    test_combat = Combat(monsters=[kenku, kenku, goblin, goblin, goblin])
    test_wounded_creature = test_combat.fighters[2]
    test_combat.wounded_fighters[2] = True

    index = 0
    while test_combat.fighters[index].name == test_wounded_creature.name:
        index += 1
    test_opponent = test_combat.fighters[index].find_opponent(
        fighters=test_combat.fighters, wounded_fighters=test_combat.wounded_fighters
    )
    try:
        assert test_opponent == 2
    except Exception as error:
        pytest.fail(f"Failed to find the wounded opponent. Error: {error}")
