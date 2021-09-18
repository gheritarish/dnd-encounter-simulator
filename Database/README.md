# Database
This folder contains the structure for the database that is used. It describes the different tables, what they contain, and how they are then used in the project.

## Structure
The structure of this database is presented in this entity-relationship diagram.

(to be uploaded)

### Weapons
The `weapons` table contains the different weapons. For each of them, it states:

* The name of the weapon
* The damage dealt by the weapon
* If the weapon has the finesse or the two-handed property
* If the weapon is a ranged weapon or not
* The type of the weapon (simple or martial weapon)

### Monsters
The `monsters` table contains the monsters existing in D&D. For each of them, it states:

* The name of the monster
* The proficiency, fixed hit points, armor classe, challenge rating of the monster
* The weapons of the monster, described as follow: `{'strength: 12', 'dexterity: 11', 'constitution: 14', 'intelligence: 3', 'wisdom: 12', 'charisma: 9'}`

### Spells
The `spells` table contains the spells existing in D&D. It presents, for each spell:

* The name of the spell
* The damage dealt by the spell
* If the spell requires an attack roll or not
* Which kind of saving throw the spell requires (`none` in case there is none)
* If the spell is a concentration spell or not
* The conditions applied by the spell

### Conditions
The `conditions` table contains the different conditions, with their names.

## How is the database used
To be written.
