import pandas as pd
import psycopg2
import os
import glob
from conversational_txt2sql import get_config

DEFAULT_DB_CONFIG = get_config()["DEFAULT_DB_CONFIG"]


def execute_sql_query(sql_query, db_name, db_config=None) -> pd.DataFrame:
    """
    Executes a SQL query on the specified PostgreSQL database and returns the result.

    Args:
        sql_query (str): The SQL query to execute.
        db_name (str): The name of the database.
        db_config (dict, optional): Database configuration parameters.

    Returns:
        df: The result of the query as a Dataframe.
    """
    # Use the provided db_config or fall back to the default configuration
    db_config = db_config or DEFAULT_DB_CONFIG

    # Add the database name to the connection parameters
    conn_params = {
        "dbname": f"{db_name}_template",
        "user": db_config["user"],
        "password": db_config["password"],
        "host": db_config["host"],
        "port": db_config["port"],
    }

    try:
        # Establish a connection to the database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all results
        result = cursor.fetchall()

        # Fetch Column names
        colnames = [desc[0] for desc in cursor.description]

        # Create a dataframe
        df = pd.DataFrame(result, columns=colnames)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return df

    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()


def initialize_database(dump_folder, db_name, db_config=None):
    """
    Initializes the database by loading all .sql dump files from the specified folder.

    Args:
        dump_folder (str): Path to the folder containing .sql dump files.
        db_name (str): The name of the database.
        db_config (dict, optional): Database configuration parameters.
    """
    dump_folder = os.path.join(dump_folder, f"{db_name}_template")
    # Use the provided db_config or fall back to the default configuration
    db_config = db_config or DEFAULT_DB_CONFIG

    # Add the database name to the connection parameters
    conn_params = {
        "dbname": "db_name",
        "user": db_config["user"],
        "password": db_config["password"],
        "host": "localhost",
        "port": db_config["port"],
    }

    try:
        # Establish a connection to the database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Find all .sql files in the dump folder
        sql_files = glob.glob(os.path.join(dump_folder, "*.sql"))

        if not sql_files:
            print(f"No .sql files found in {dump_folder}")
            return

        # Execute each .sql file
        for sql_file in sql_files:
            print(f"Loading {sql_file} into database {db_name}...")
            with open(sql_file, "r") as file:
                sql_commands = file.read()
                cursor.execute(sql_commands)
                conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print(f"Database {db_name} initialized successfully.")

    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
