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
        immunities: List[str],
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
        self.immunities = [immunity for immunity in immunities]
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

    def damage(self, damages: int, type_of_damage: str):
        """
        Method to remove HP when a Creature takes a hit.

        :param damages: (int) The quantity of damage done
        :param type_of_damage: (str) The type of damage dealt by the attack
        """
        if type_of_damage in self.resistances:
            self.hit_points -= damages // 2
        elif type_of_damage in self.immunities:
            self.hit_points = self.hit_points
        elif type_of_damage in self.vulnerabilities:
            self.hit_points -= damages * 2
        else:
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
            logger.warning(f"Error: {error}, weapon not changed")


class Monster(Creature):
    def __init__(
        self,
        name: str,
        hit_points: int,
        armor_class: int,
        stats: Dict,
        weapons: List[Weapon],
        resistances: List[str],
        immunities: List[str],
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
            immunities=immunities,
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
            opponent.damage(damages=damage_dealt, type_of_damage=weapon.type_of_damage)

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

    def find_best_weapon(
        self,
        known_resistances: List[str] = [],
        known_immunities: List[str] = [],
        known_vulnerabilities: List[str] = [],
    ) -> int:
        """
        Method to find the best weapon (ie deals statistically the more damage)

        #TODO: add options and limitations for two-handed, ranged, damage immunity...

        :return: (int) the index of the best weapon to use
        """
        if len(self.weapons) == 0:
            raise IndexError("This monster has no weapon.")

        best_weapon = 0
        if self.weapons[best_weapon].type_of_damage in known_resistances:
            best_mean = self.weapons[best_weapon].average_damage() / 2
        elif self.weapons[best_weapon].type_of_damage in known_immunities:
            best_mean = 0
        elif self.weapons[best_weapon].type_of_damage in known_vulnerabilities:
            best_mean = self.weapons[best_weapon].average_damage() * 2
        else:
            best_mean = self.weapons[best_weapon].average_damage()

        for (index, weapon) in enumerate(self.weapons):
            if weapon.type_of_damage in known_resistances:
                temporary_mean = weapon.average_damage() / 2
            elif weapon.type_of_damage in known_immunities:
                temporary_mean = 0
            elif weapon.type_of_damage in known_vulnerabilities:
                temporary_mean = weapon.average_damage() * 2
            else:
                temporary_mean = weapon.average_damage()

            # comparison by max damage possible. No change if both means are identical
            if temporary_mean > best_mean:
                best_weapon = index
                best_mean = temporary_mean
        return best_weapon
