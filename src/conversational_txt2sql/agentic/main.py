#!/usr/bin/env python
import argparse
import logging

from conversational_txt2sql.agentic.crew import ConversationalText2SQLCrew
from conversational_txt2sql.prompt import get_db_schema_and_metadata

logging.basicConfig(level=logging.INFO)


def run(user_question: str = None):
    """
    Run the crew, extract generated SQL and any executed dataframe output.
    Args:
        user_question: optional user question to run against the DB schema. If None, a default question is used.
    Returns:
        dict with keys: generated_sql (first), executed_df (pandas.DataFrame or None).
    """

    inputs = get_db_schema_and_metadata(
        DATASET_PATH="data/table_schema_info",
        db="exchange_traded_funds",
    )

    if user_question is None:
        user_question = (
            "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? "
            "For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
        )

    inputs["user_question"] = user_question

    try:
        crew_result = ConversationalText2SQLCrew().crew().kickoff(inputs=inputs)
    except Exception:
        logging.exception("Crew kickoff failed")
        raise

    # collect SQL(s) produced by the "generate_sql" task(s)
    all_sql = [
        getattr(t.pydantic, "sql", None)
        for t in crew_result.tasks_output
        if getattr(t, "name", "") == "generate_sql"
    ]
    all_sql = [s for s in all_sql if s]  # filter out None/empty
    logging.info("Generated %d SQL statement(s)", len(all_sql))

    # attempt to find an executed dataframe from known task names
    all_executed_df = [
        getattr(t.pydantic, "df_output", None)
        for t in crew_result.tasks_output
        if getattr(t, "name", "") == "execute_debug_sql"
    ]

    return {
        "generated_sql": all_sql[0] if all_sql else None,
        "executed_df": all_executed_df[0] if all_executed_df else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run ConversationalText2SQL crew with a custom user question."
    )
    parser.add_argument(
        "--question", "-q", type=str, help="User question to parametrize the run."
    )
    args = parser.parse_args()
    result = run(user_question=args.question)
    logging.info("Result: %s", result)
