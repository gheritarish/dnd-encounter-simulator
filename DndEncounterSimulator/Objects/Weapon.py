import dice


class Weapon:
    def __init__(self, name: str, stat_to_hit: str, damage: str):
        self.name = str(name)
        self.stat_to_hit = str(stat_to_hit)
        self.damage = str(damage)

    def critical_hit(self) -> str:
        """
        Method to automatically compute the damage for a critical hit.

        :return: The dice to roll for a critical hit.
        """
        dice_critical_hit = 2 * int(self.damage.split("d")[0])
        value_of_dice = self.damage.split("d")[1]
        damage_critical = "d".join([str(dice_critical_hit), value_of_dice])
        return damage_critical

    def deal_damage(self, modifier: int, critical_hit: bool) -> int:
        """
        Method to compute the damage dealt by a weapon.

        :param modifier: (int) The modifier to damage from the creature.
        :param critical_hit: (bool) A boolean indicating if the hit is a crit or not.

        :return: (int) The number of damage dealt
        """
        if critical_hit:
            damage_dice = self.critical_hit()
        else:
            damage_dice = self.damage
        damage = dice.roll(damage_dice)[0] + modifier
        return damage
