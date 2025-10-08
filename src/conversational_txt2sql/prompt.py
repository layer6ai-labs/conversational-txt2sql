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


def generate_prompt(DATASET_PATH, question, db):
    """Generate a prompt for the LLM based on the question and database context."""
    with open(os.path.join(DATASET_PATH, db, f"{db}_schema.txt"), "r") as file:
        db_schema = file.read()

    with open(
        os.path.join(DATASET_PATH, db, f"{db}_column_meaning_base.json"), "r"
    ) as file:
        column_descriptions = file.read()

    with open(os.path.join(DATASET_PATH, db, f"{db}_kb.jsonl"), "r") as file:
        knowledge = file.read()

    return system_prompt.format(
        db_schema=db_schema,
        column_descriptions=column_descriptions,
        knowledge=knowledge,
        question=question,
    )
