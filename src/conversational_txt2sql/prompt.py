import os

system_prompt = """
You are an expert at converting natural language questions into SQL queries. Given a user's question and the context of the database schema, your task is to generate an accurate SQL query that retrieves the desired information.
Use the following guidelines to construct your SQL query:
1. Understand the user's question thoroughly, identifying key entities, attributes, and conditions.
2. Analyze the provided database schema context to determine the relevant tables and columns.
3. Construct a SQL query that accurately reflects the user's intent, ensuring it is syntactically correct and efficient.
4. If the question is ambiguous, make reasonable assumptions based on common practices in database querying.

Format your response as a single SQL query within <SQL></SQL> without any additional explanations or comments.

Database Schema Context:
{db_schema}

Column meanings and descriptions (if any):
{column_descriptions}

External knowledge (if any):
{knowledge}

User's Question:
{question}

SQL Query:
<SQL> your SQL query here </SQL>
"""


def get_db_schema_and_metadata(DATASET_PATH: str, db: str):
    """
    Loads the database schema, column descriptions, and external knowledge for a given database.

    Args:
        DATASET_PATH: Path to the dataset directory
        db: Database name

    Returns:
        Tuple of (db_schema, column_descriptions, knowledge)
    """
    with open(os.path.join(DATASET_PATH, db, f"{db}_schema.txt"), "r") as file:
        db_schema = file.read()

    with open(
        os.path.join(DATASET_PATH, db, f"{db}_column_meaning_base.json"), "r"
    ) as file:
        column_descriptions = file.read()

    with open(os.path.join(DATASET_PATH, db, f"{db}_kb.jsonl"), "r") as file:
        knowledge = file.read()

    return {
        "db": db,
        "db_schema": db_schema,
        "column_descriptions": column_descriptions,
        "knowledge": knowledge,
    }


def generate_prompt(DATASET_PATH: str, question: str, db: str) -> str:
    """
    Generates a formatted prompt for an LLM to convert a user question into an SQL query,
    using the database schema, column descriptions, and external knowledge for a given database.

    Args:
        DATASET_PATH (str): Path to the dataset directory.
        question (str): The user's natural language question.
        db (str): The name of the database.

    Returns:
        str: The formatted prompt string for the LLM.
    """
    db_schema_metadata = get_db_schema_and_metadata(DATASET_PATH, db)
    return system_prompt.format(
        db_schema=db_schema_metadata["db_schema"],
        column_descriptions=db_schema_metadata["column_descriptions"],
        knowledge=db_schema_metadata["knowledge"],
        question=question,
    )
