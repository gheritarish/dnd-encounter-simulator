import argparse

from loguru import logger
from tqdm import tqdm

from DndEncounterSimulator.Objects.Combat import Combat
from DndEncounterSimulator.Objects.Creature import Monster
from DndEncounterSimulator.Objects.Weapon import DamageType, Weapon
from DndEncounterSimulator.Tools.utils.Stats import STATS_GOBLIN, STATS_KENKU


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--simulations",
        "-s",
        type=int,
        help="Number of simulations to run",
        default=100,
    )
    args = parser.parse_args()
    return args


def main():
    args = define_args()

    goblin_victories = 0
    kenku_victories = 0
    for _ in tqdm(range(args.simulations)):
        scimitar = Weapon(
            name="scimitar",
            stat_to_hit="dexterity",
            damage="1d6",
            type_of_damage=DamageType(name="slashing"),
        )
        goblin = Monster(
            name="goblin",
            hit_points=7,
            armor_class=15,
            stats=STATS_GOBLIN,
            weapons=[scimitar],
            resistances=[],
            immunities=[],
            vulnerabilities=[],
            proficiency=2,
            camp="blue",
        )

        shortsword = Weapon(
            name="shortsword",
            stat_to_hit="dexterity",
            damage="1d6",
            type_of_damage=DamageType(name="slashing"),
        )
        kenku = Monster(
            name="kenku",
            hit_points=13,
            armor_class=13,
            stats=STATS_KENKU,
            weapons=[shortsword],
            resistances=[],
            immunities=[],
            vulnerabilities=[],
            proficiency=2,
            camp="red",
        )

        combat = Combat(monsters=[kenku, goblin])
        victorious_camp = combat.fight()

        if victorious_camp == "blue":
            goblin_victories += 1
        else:
            kenku_victories += 1

    logger.info(
        f"Kenku victories: {kenku_victories}, goblin victories: {goblin_victories}"
    )


if __name__ == "__main__":
    main()
