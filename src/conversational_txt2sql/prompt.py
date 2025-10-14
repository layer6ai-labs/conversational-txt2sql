import os

SUMMARIZE_CLARIFICATIONS_PROMPT = """
You are an intelligent agent specializing in synthesizing user intent for complex tasks. Your role is to carefully integrate the original user question with all clarifications exchanged during the conversation. Each clarification is provided on a new line.

Your output should be a single, clear, and comprehensive summary that unifies the key information, constraints, and goals communicated by the user—including all implicit and explicit requirements inferred from clarifications. The summary should reflect the user's fully clarified intent, expressed so it is actionable for tasks such as generating high-quality SQL queries.

Ensure your summary:
- Is concise yet sufficiently detailed.
- Preserves every essential specification or constraint from the original question and clarifications.
- Omits irrelevant or redundant information.
- Is written in a neutral and informative tone.

Include relevant database context for maximum clarity.

Database Schema Context:
{db_schema}

Column meanings and descriptions (if any):
{column_descriptions}

External knowledge (if any):
{knowledge}

All User Inputs (Original Question plus any Clarifications):
{question}

Unified Intent Summary (your output):

"""

AMBIGUITY_PROMPT = """
You are assisting in determining whether a user's question can be directly answered by converting it into an SQL query, given the following database context.

Instructions:
1. If the user's question is unrelated to the information available in the provided database schema, column descriptions, or external knowledge, respond with a JSON object: 
"clarity": "unrelated", "clarifying_question": "I can only answer questions based on the provided database schema and information. Please ask a relevant question."
2. If essential information is missing, the question could have multiple interpretations, or is otherwise ambiguous, respond with a JSON object: "clarity": "not clear", "clarifying_question": "<Pose a single, concrete clarifying question based on the provided context that would help resolve the ambiguity and enable you to generate a precise SQL query>"
3. If the question is explicit, relevant to the database, and has all information needed to generate a SQL query, respond with a JSON object: "clarity": "clear", "clarifying_question": ""

Your response must be a JSON object with the following fields:

  "clarity": "clear" or "not clear",
  "clarifying_question": string (a clarifying question, or an empty string if not needed)

Return only JSON object enclosed in curly braces.


Database Schema Context:
{db_schema}

Column meanings and descriptions (if any):
{column_descriptions}

External knowledge (if any):
{knowledge}

User's Question:
{question}
"""


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


def generate_prompt(
    DATASET_PATH: str, question: str, db: str, system_prompt: str = system_prompt
) -> str:
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
