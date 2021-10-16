from typing import List

from DndEncounterSimulator.Objects.Creature import Monster


class Combat:
    def __init__(self, monsters: List[Monster]):
        self.fighters = monsters
        self.sort_initiatives()
        self.wounded_fighters = [False for _ in self.fighters]

    def sort_initiatives(self):
        """
        Method to sort the initiatives of the creatures in a fight.
        """
        self.fighters.sort(key=lambda x: x.initiative, reverse=True)

    def is_over(self) -> bool:
        """
        Method to know if the fight is over or not.
        This method searches if there are still opponents from other camps,
        returns False if it finds any opponent, False otherwise.

        :return: (bool) True if the fight is over, False otherwise.
        """
        if isinstance(
            self.fighters[0].find_opponent(self.fighters, self.wounded_fighters), int
        ):
            return False
        else:
            return True

    def fight(self) -> str:
        """
        Method to run the fight. It returns the color of the winning camp.

        :return: (str) The color of the winning camp
        """
        while not self.is_over():
            for fighter in self.fighters:
                index_opponent = fighter.find_opponent(
                    self.fighters, self.wounded_fighters
                )
                if isinstance(index_opponent, int):
                    fighter.attack(
                        self.fighters[index_opponent],
                        weapon=fighter.weapons[0],
                    )
                    self.wounded_fighters[index_opponent] = True
                    if self.fighters[index_opponent].dead:
                        self.fighters.pop(index_opponent)
                else:
                    return self.fighters[0].camp
        return self.fighters[0].camp
