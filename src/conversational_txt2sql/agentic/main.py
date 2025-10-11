#!/usr/bin/env python
import os

from conversational_txt2sql.agentic.crew import ConversationalText2SQLCrew
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

    ConversationalText2SQLCrew().crew().kickoff(inputs=inputs)
