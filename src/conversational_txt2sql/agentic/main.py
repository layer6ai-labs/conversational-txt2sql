#!/usr/bin/env python
from conversational_txt2sql.agentic.planner_crew import ConversationalText2SQLCrew
from conversational_txt2sql.prompt import get_db_schema_and_metadata


def run():
    """
    Run the crew.
    """
    inputs = get_db_schema_and_metadata(
        DATASET_PATH="/home/abinavrameshs/projects/scratch/conversational-txt2sql/data/table_schema_info",
        db="exchange_traded_funds",
    )
    inputs["user_question"] = (
        "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
    )

    crew_result = ConversationalText2SQLCrew().crew().kickoff(inputs=inputs)


# # Will give the result of the resultant table (executed SQL query)
# import pandas as pd
# pd.DataFrame(crew_result.pydantic.df_output)

# # You can also access the task output like as follows:
# for task_output in crew_result.tasks_output:
#     if task_output.name =="execute_debug_sql":
#        table_output = pd.DataFrame(task_output.pydantic.df_output)
