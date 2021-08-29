class Weapon:
    def __init__(self, stat_to_hit: str, damage: str):
        self.stat_to_hit = str(stat_to_hit)
        self.damage = str(damage)

    def critical_hit(self) -> str:
        """
        Method to automatically compute the damage for a critical hit.

        :return: The dice to roll for a critical hit.
        """
        dice_critical_hit = 2*int(self.damage.split("d")[0])
        value_of_dice = self.damage.split("d")[1]
        damage_critical = "d".join([str(dice_critical_hit), value_of_dice])
        return damage_critical
