from typing import List

from DndEncounterSimulator.Objects.Creature import Monster


def sort_initiatives(opponents: List[Monster]):
    opponents.sort(key=lambda x: x.initiative)
    return opponents
