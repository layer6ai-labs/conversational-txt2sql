from typing import Any

from crewai.tools import tool

from conversational_txt2sql import get_config
from conversational_txt2sql.database_utils import execute_sql_query

DEFAULT_DB_CONFIG = get_config()["DEFAULT_DB_CONFIG"]


# , result_as_answer=True
@tool("execute_sql_query_tool")
def execute_sql_query_tool(
    sql_query: str, db_name: str, db_config: None | dict[str, Any] = DEFAULT_DB_CONFIG
) -> str:
    """
    Executes a given SQL query on the specified PostgreSQL database and returns the query result.

    This tool is intended to be used by agents who need to run SQL statements (SELECT, etc.) on a database and retrieve the query result for further processing or analysis. The result is returned as a pandas DataFrame for easy data manipulation and inspection.

    Args:
        sql_query (str): The SQL query to be executed (e.g., SELECT statement).
        db_name (str): The name of the target database.
        db_config (dict, optional): A dictionary of database configuration options. If not provided, the default configuration will be used.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the executed SQL query.

    Raises:
        psycopg2.Error: Raised if an error occurs during connection or execution of the SQL query.
        Exception: Other generic exceptions may occur, for example if a non-SELECT statement is executed or the connection fails unexpectedly.

    """
    return execute_sql_query(sql_query, db_name, db_config)
