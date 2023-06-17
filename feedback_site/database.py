"""database.py is the database layer for the feedback site."""
from typing import Any
import psycopg2


# Define connection parameters
DB_CONFIG = {
    "database": "test_database",
    "user": "test_user",
    "password": "test@123",
    "host": "127.0.0.1",
    "port": "5432",
}


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Establish and return a connection with the database.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return 0


def execute_query(query: str, *params: Any):
    """
    Execute a query with given parameters and return the result.

    query: SQL query to be executed
    params: parameters to be used with the query
    returns the query results as a list of tuples
    """
    conn = get_db_connection()
    if conn is None:
        print("Failed to establish database connection.")
        return []

    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute the query with provided parameters
        cur.execute(query, params)

        # Make sure to commit changes for INSERT statements
        if "INSERT" in query:
            conn.commit()
            return 1

        # Fetch one result
        result = cur.fetchone()

        # get rid of tuple and return
        return result[0] if result else None
    except psycopg2.Error as error:
        print(f"Error while executing query: {error}")
        return []
    finally:
        # Close communication with the database
        if cur:
            cur.close()
        if conn:
            conn.close()