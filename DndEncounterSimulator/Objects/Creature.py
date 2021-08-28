from typing import Dict

import dice

from DndEncounterSimulator.Objects.utils.conversion import convert_stat_to_mod


class Creature:
    """
    A class to define all kind of creatures that might be encountered.
    """

    def __init__(self, hit_points: int, armor_class: int, stats: Dict):
        self.hit_points = int(hit_points)
        self.armor_class = int(armor_class)
        if stats:
            self.stats = {
                "strength": int(stats["strength"]),
                "dexterity": int(stats["dexterity"]),
                "constitution": int(stats["constitution"]),
                "intelligence": int(stats["intelligence"]),
                "wisdom": int(stats["wisdom"]),
                "charisma": int(stats["charisma"]),
            }
        self.weapons = {"damage": "1d6"}
        self.modifiers = {
            key: convert_stat_to_mod(value) for (key, value) in self.stats.items()
        }


class Monster(Creature):
    def __init__(
        self, hit_points: int, armor_class: int, stats: Dict, proficiency: int
    ):
        super(Monster, self).__init__(
            hit_points=hit_points,
            armor_class=armor_class,
            stats=stats,
        )
        self.proficiency = int(proficiency)

    def attack(self, opponent: Creature):
        """
        Method simulating the attack of a monster on a Creature

        :param opponent: (Creature) The target of the attack.
        """
        critical_hit = False

        dice_roll = dice.roll("1d20")[0]
        to_hit = dice_roll + self.proficiency + self.modifiers["strength"]

        if to_hit >= opponent.armor_class:
            hit = True
            if dice_roll == 20:
                critical_hit = True
        else:
            hit = False
        if hit:
            if critical_hit:
                opponent.hit_points -= (
                    dice.roll(self.weapons["damage"])[0]
                    + dice.roll(self.weapons["damage"])[0]
                    + self.modifiers["strength"]
                )
            else:
                opponent.hit_points -= (
                    dice.roll(self.weapons["damage"])[0] + self.modifiers["strength"]
                )
