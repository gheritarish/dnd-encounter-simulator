"""
Script to initialize the database by creating the tables, sequences and constraints.

Args:
    --database: (str) The name of the database on which to implement the schema
    --user: (str) The user connecting to the database, postgres is the default
    --port: (int) The port on which the database is, 5432 is the default
    --password: (str) The password to connect to the database
    --host: (str) The host on which the database is, localhost is the default
"""
import argparse
import sys

from loguru import logger

from DndEncounterSimulator.Objects.Database import Database


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database", type=str, help="The name of the database", default=None
    )
    parser.add_argument(
        "--user", "-u", type=str, help="The identifiant of the user", default="postgres"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="The port to connect to the database",
        default=5432,
    )
    parser.add_argument(
        "--password",
        type=str,
        help="The password to connect to the database",
        default=None,
    )
    parser.add_argument(
        "--host", type=str, help="The host of the database", default="localhost"
    )
    args = parser.parse_args()
    return args


def main():
    args = define_args()
    database = Database(
        user=args.user,
        database=args.database,
        password=args.password,
        host=args.host,
        port=args.port,
    )

    if database.is_valid():
        sql_file = open("./database_initialization.sql")
        sql_as_string = sql_file.read()
        try:
            database.execute_query(sql_as_string)
            database.commit()
        except Exception as error:
            database.rollback()
            logger.warning(error)
    else:
        logger.error("Failed to connect to the database")
        sys.exit()


if __name__ == "__main__":
    main()
