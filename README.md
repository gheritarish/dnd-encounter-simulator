# D&D encounter simulator
How many times did you, as a DM, discover that the encounter you spent dozens of minutes preparing was far too easy for your group? Or that, on the contrary, the encounter that was supposed to be of a medium difficulty was for too hard and that your players stood no chance? 

The objective of this simulator is to help you try the encounters before they really happen. Indeed, if simulating them by hand works, it is *long*, and simulating them using probabilities doesn't take into account the fact that dice, sometimes, act on their own logic.

## What do we expect to achieve with this project?
The final objective is to be able to simulate encounters, with the party on one side, and the enemies they face on the other.

In its final state, the project should be able to take into account *everything* that players can use.

But for now, the focus is far simpler: allow the simulation of fights, using only weapons, and nothing else.

## Installation
This project works with `python3`. To install it, follow these steps:

* Clone the repository from the command line (`git clone https/ssh_link`). This will download the repository and all its content in a folder named `dnd-encounter-simulator`.
* Without moving, use `pip install --editable ./dnd-encounter-simulator`. This will allow the modifications you make to be directly taken into account, without having to re-install the project each time.
* You're good to go. Open python and `import DndEncounterSimulator` can run (or anything if you want to import only specific parts in your code).
