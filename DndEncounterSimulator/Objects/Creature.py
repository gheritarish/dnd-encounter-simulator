from typing import Dict, List

import dice

from DndEncounterSimulator.Objects.utils.conversion import convert_stat_to_mod
from DndEncounterSimulator.Objects.Weapon import Weapon


class Creature:
    """
    A class to define all kind of creatures that might be encountered.
    """

    def __init__(
        self,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
    ):
        self.hit_points = int(hit_points)
        self.armor_class = int(armor_class)
        if stats:
            self.stats = stats
        self.weapons = [weapon for weapon in weapons]
        self.modifiers = {
            key: convert_stat_to_mod(value) for (key, value) in self.stats.items()
        }
        self.dead = False

    def roll_initiative(self) -> int:
        """
        Method to roll the initiative of a creature.

        :return: (int) The initiative rolled.
        """
        initiative = dice.roll("1d20")[0] + self.modifiers["dexterity"]
        return initiative

    def damage(self, damages: int):
        """
        Method to remove HP when a Creature takes a hit.

        :param damages: (int) The quantity of damage done
        """
        self.hit_points -= damages
        if self.hit_points <= 0:
            self.dead = True


class Monster(Creature):
    def __init__(
        self,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        proficiency: int,
    ):
        super(Monster, self).__init__(
            hit_points=hit_points,
            armor_class=armor_class,
            stats=stats,
            weapons=weapons,
        )
        self.proficiency = int(proficiency)

    def attack(self, opponent: Creature, weapon: Weapon):
        """
        Method simulating the attack of a monster on a Creature

        :param opponent: (Creature) The target of the attack.
        :param weapon: (Weapon) The weapon used to attack the enemy.
        """
        critical_hit = False

        dice_roll = dice.roll("1d20")[0]
        to_hit = dice_roll + self.proficiency + self.modifiers[weapon.stat_to_hit]

        if to_hit >= opponent.armor_class:
            hit = True
            if dice_roll == 20:
                critical_hit = True
        else:
            hit = False

        if hit:
            if critical_hit:
                opponent.damage(
                    dice.roll(weapon.critical_hit())[0]
                    + self.modifiers[weapon.stat_to_hit]
                )
            else:
                opponent.damage(
                    dice.roll(weapon.damage)[0] + self.modifiers[weapon.stat_to_hit]
                )
