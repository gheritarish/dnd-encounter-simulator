-- Create enum for weapon types
DROP TYPE IF EXISTS weapon_type CASCADE;
CREATE TYPE weapon_type AS ENUM
    ('simple', 'martial');

ALTER TYPE weapon_type
    OWNER TO postgres;

-- Create sequence for weapon id
DROP SEQUENCE IF EXISTS public.weapon_id_seq CASCADE;
CREATE SEQUENCE public.weapon_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 1000
    CACHE 1;

-- Create table to store weapons
DROP TABLE IF EXISTS public.weapons;
CREATE TABLE public.weapons
(
    id_weapon INTEGER NOT NULL DEFAULT nextval('public.weapon_id_seq'::regclass),
    name_weapon CHARACTER VARYING,
    damage CHARACTER VARYING,
    type weapon_type NOT NULL,
    finesse BOOLEAN,
    two_handed BOOLEAN,
    ranged BOOLEAN
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.weapons ADD CONSTRAINT weapon_pkey
PRIMARY KEY (id_weapon);

GRANT ALL ON public.weapons TO postgres;


-- Create sequence for monster id
DROP SEQUENCE IF EXISTS public.monster_id_seq CASCADE;
CREATE SEQUENCE public.monster_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 10000
    CACHE 1;

-- Create table to store monsters
DROP TABLE IF EXISTS public.monsters;
CREATE TABLE public.monsters
(
    id_monster INTEGER NOT NULL DEFAULT nextval('public.monster_id_seq'::regclass),
    name_monster CHARACTER VARYING,
    proficiency INTEGER,
    hit_points INTEGER,
    armor_class INTEGER,
    stats CHARACTER VARYING[],
    challenge_rating CHARACTER VARYING
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.monsters ADD CONSTRAINT monster_pkey
PRIMARY KEY (id_monster);

GRANT ALL ON public.monsters TO postgres;


-- Create enum for saving throw types
DROP TYPE IF EXISTS saving_throw_type CASCADE;
CREATE TYPE saving_throw_type AS ENUM
    ('strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma',
    'none'
);

ALTER TYPE saving_throw_type
    OWNER TO postgres;

-- Create sequence for spell id
DROP SEQUENCE IF EXISTS public.spell_id_seq CASCADE;
CREATE SEQUENCE public.spell_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 10000
    CACHE 1;

-- Create table to store spells
DROP TABLE IF EXISTS public.spells;
CREATE TABLE public.spells
(
    id_spell INTEGER NOT NULL DEFAULT nextval('public.spell_id_seq'::regclass),
    name_spell CHARACTER VARYING,
    modifier BOOLEAN,
    attack BOOLEAN,
    saving_throw saving_throw_type NOT NULL DEFAULT 'none',
    condition_id INTEGER,
    concentration BOOLEAN
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.spells ADD CONSTRAINT spell_pkey
PRIMARY KEY (id_spell);

GRANT ALL ON public.spells TO postgres;


-- Create sequence for condition id
DROP SEQUENCE IF EXISTS public.condition_id_seq CASCADE;
CREATE SEQUENCE public.condition_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 100
    CACHE 1;

-- Create table to store conditions
DROP TABLE IF EXISTS public.conditions;
CREATE TABLE public.conditions
(
    id_condition INTEGER NOT NULL DEFAULT nextval('public.condition_id_seq'::regclass),
    name_condition CHARACTER VARYING
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.conditions ADD CONSTRAINT condition_pkey
PRIMARY KEY (id_condition);

GRANT ALL ON public.conditions TO postgres;

-- Add foreign key for condition applied by spell
ALTER TABLE public.spells ADD CONSTRAINT fk_id_condition
FOREIGN KEY (condition_id) REFERENCES public.conditions (id_condition) MATCH SIMPLE ON
UPDATE CASCADE ON
DELETE CASCADE;