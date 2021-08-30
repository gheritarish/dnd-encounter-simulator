import logging
import argparse

from tqdm import tqdm

from DndEncounterSimulator.Objects.Creature import Monster
from DndEncounterSimulator.Objects.Weapon import Weapon
from DndEncounterSimulator.Tools.utils.Stats import (
    STATS_KENKU,
    STATS_GOBLIN,
)


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
    logging.getLogger().setLevel(logging.INFO)
    args = define_args()

    goblin_victories = 0
    kenku_victories = 0
    for _ in tqdm(range(args.simulations)):
        scimitar = Weapon(stat_to_hit="dexterity", damage="1d6")
        goblin = Monster(
            hit_points=7,
            armor_class=15,
            stats=STATS_GOBLIN,
            weapons=[scimitar],
            proficiency=2,
        )

        shortsword = Weapon(stat_to_hit="dexterity", damage="1d6")
        kenku = Monster(
            hit_points=13,
            armor_class=13,
            stats=STATS_KENKU,
            weapons=[shortsword],
            proficiency=2,
        )

        initiative_goblin = goblin.roll_initiative()
        initiative_kenku = kenku.roll_initiative()

        while initiative_kenku == initiative_goblin:
            initiative_goblin = goblin.roll_initiative()
            initiative_kenku = kenku.roll_initiative()

        if initiative_kenku > initiative_goblin:
            while not (goblin.is_dead() or kenku.is_dead()):
                kenku.attack(opponent=goblin, weapon=kenku.weapons[0])
                if not goblin.is_dead():
                    goblin.attack(opponent=kenku, weapon=goblin.weapons[0])

        elif initiative_goblin > initiative_kenku:
            while not (goblin.is_dead() or kenku.is_dead()):
                goblin.attack(opponent=kenku, weapon=goblin.weapons[0])
                if not kenku.is_dead():
                    kenku.attack(opponent=goblin, weapon=kenku.weapons[0])

        if kenku.is_dead():
            goblin_victories += 1
        else:
            kenku_victories += 1

    logging.info(f"Kenku victories: {kenku_victories}, goblin victories: {goblin_victories}")


if __name__ == "__main__":
    main()
