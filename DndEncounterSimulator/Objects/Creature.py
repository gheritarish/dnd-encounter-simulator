from typing import Dict

import dice


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
        to_hit = dice.roll("1d20")[0] + self.proficiency + self.stats["strength"]
        if to_hit >= opponent.armor_class:
            hit = True
        else:
            hit = False
        if hit:
            opponent.hit_points -= (
                dice.roll(self.weapons["damage"])[0] + self.stats["strength"]
            )
