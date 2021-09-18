import logging
import psycopg2
import psycopg2.extras


class Database:
    def __init__(
        self,
        user: str,
        database: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        connection=None
    ):
        self.params = {
            "user": user,
            "database": database,
            "password": password,
            "host": host,
            "port": port,
        }
        self.connection = connection
        self.cursor = None
        self.set_connection()

    def set_connection(self):
        if self.params:
            try:
                conn = psycopg2.connect(**self.params)
                self.connection = conn
            except Exception as error:
                logging.error(error)

        if self.connection:
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch_query_results(self, query):
        self.execute_query(query)
        return self.cursor.fetchall()

    def fetch_query_data_results(self, query, data):
        self.execute_query_data(query, data)
        return self.cursor.fetchall()

    def execute_query(self, query):
        if self.cursor.closed:
            self.set_connection()
        self.cursor.execute(query)

    def execute_query_data(self, query, data):
        if self.cursor.closed:
            self.set_connection()
        self.cursor.execute(query, data)

    def is_valid(self):
        try:
            self.set_connection()
        except Exception as error:
            logging.error(error)
            return False
        if self.cursor:
            return True
        else:
            return False
