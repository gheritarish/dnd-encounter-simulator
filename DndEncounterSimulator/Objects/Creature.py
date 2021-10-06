from typing import Dict, List, Union

import dice
from loguru import logger

from DndEncounterSimulator.Objects.utils.conversion import convert_stat_to_mod
from DndEncounterSimulator.Objects.Weapon import Weapon


class Creature:
    """
    A class to define all kind of creatures that might be encountered.
    """

    def __init__(
        self,
        name: str,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        resistances: List[str],
        vulnerabilities: List[str],
        camp: str,
    ):
        self.name = name
        self.hit_points = int(hit_points)
        self.armor_class = int(armor_class)
        if stats:
            self.stats = stats
        self.weapons = [weapon for weapon in weapons]
        self.modifiers = {
            key: convert_stat_to_mod(value) for (key, value) in self.stats.items()
        }
        self.resistances = [resistance for resistance in resistances]
        self.vulnerabilities = [vulnerability for vulnerability in vulnerabilities]
        self.dead = False
        self.initiative = self.roll_initiative()
        self.camp = str(camp)

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

    def change_weapon(self, index: int):
        """
        Method to change to the weapon referenced by the index: this weapon will be placed at index 0 for use in combat

        :param index: (int) the index referencing a weapon in weapons list
        """
        try:
            choice = self.weapons.pop(index)
            self.weapons.insert(0, choice)
        except Exception as error:
            logger.info(f"Error: {error}, weapon not changed")


class Monster(Creature):
    def __init__(
        self,
        name: str,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        resistances: List[str],
        vulnerabilities: List[str],
        proficiency: int,
        camp: str,
    ):
        super(Monster, self).__init__(
            name=name,
            hit_points=hit_points,
            armor_class=armor_class,
            stats=stats,
            weapons=weapons,
            resistances=resistances,
            vulnerabilities=vulnerabilities,
            camp=camp,
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

        if dice_roll == 20:
            critical_hit = True
            hit = True
        elif to_hit >= opponent.armor_class:
            hit = True
        else:
            hit = False

        if hit:
            damage_dealt = weapon.deal_damage(
                modifier=self.modifiers[weapon.stat_to_hit], critical_hit=critical_hit
            )
            opponent.damage(damage_dealt)

    def find_opponent(self, fighters: List[Creature]) -> Union[None, int]:
        """
        Method to find which opponent to fight in a list of creatures.
        This method finds an opponent of another camp, so it doesn't attack an ally.

        :param fighters: (List[Creatures]) the list of creatures in the fight.
        :return: (Union[None, int]) the index of the first enemy found, None otherwise.
        """
        for (index, fighter) in enumerate(fighters):
            if fighter.camp != self.camp:
                return index
        return None

    def find_best_weapon(self) -> int:
        """
        Method to find the best weapon (ie deals statistically the more damage)

        #TODO: add options and limitations for two-handed, ranged, damage immunity...

        :return: (int) the index of the best weapon to use
        """
        best_weapon = 0  # we assume we have at least one weapon
        best_damage = self.weapons[best_weapon].damage
        best_sum = int(best_damage.split("d")[0]) * int(best_damage.split("d")[1])
        for (index, weapon) in enumerate(self.weapons):
            temporary_damage = weapon.damage
            temporary_sum = int(temporary_damage.split("d")[0]) * int(
                temporary_damage.split("d")[1]
            )
            # comparison by max damage possible
            if temporary_sum > best_sum:
                best_weapon = index
                best_sum = temporary_sum
                best_damage = temporary_damage
            elif temporary_sum == best_sum:
                # here we chose the best weapon as having the more dice rolled: higher mean
                if int(temporary_damage.split("d")[0]) > int(best_damage.split("d")[0]):
                    best_weapon = index
                    best_sum = temporary_sum
                    best_damage = temporary_damage
        return best_weapon
