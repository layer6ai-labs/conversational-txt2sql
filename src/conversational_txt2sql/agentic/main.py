#!/usr/bin/env python
import logging

import pandas as pd

from conversational_txt2sql.agentic.crew import ConversationalText2SQLCrew
from conversational_txt2sql.prompt import get_db_schema_and_metadata


def run():
    """
    Run the crew, extract generated SQL and any executed dataframe output.
    Returns a dict with keys: crew_result, generated_sql (first), all_generated_sql, executed_df (pandas.DataFrame or None).
    """

    logging.basicConfig(level=logging.INFO)

    inputs = get_db_schema_and_metadata(
        DATASET_PATH="data/table_schema_info",
        db="exchange_traded_funds",
    )
    inputs["user_question"] = (
        "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? "
        "For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
    )

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


# # Will give the result of the resultant table (executed SQL query)
# import pandas as pd
# pd.DataFrame(crew_result.pydantic.df_output)

# # You can also access the task output like as follows:
# for task_output in crew_result.tasks_output:
#     if task_output.name =="execute_debug_sql":
#        table_output = pd.DataFrame(task_output.pydantic.df_output)
