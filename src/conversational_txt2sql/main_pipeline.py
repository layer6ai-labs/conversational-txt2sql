import sys
from typing import Dict, List, Tuple

import pandas as pd
from pydantic import BaseModel

from conversational_txt2sql.agentic.crew import ConversationalText2SQLCrew
from conversational_txt2sql.call_api import get_query_response
from conversational_txt2sql.prompt import (
    AMBIGUITY_PROMPT,
    SUMMARIZE_CLARIFICATIONS_PROMPT,
    generate_prompt,
    get_db_schema_and_metadata,
)

DATASET_PATH = "data/table_schema_info"


def get_user_input(prompt: str, default_value: str = "") -> str:
    """
    Prompt the user for input, falling back to a default value if no input is entered.
    """
    if default_value:
        display_prompt = f"{prompt} (default: '{default_value[:50]}{'...' if len(default_value) > 50 else ''}'): "
    else:
        display_prompt = f"{prompt}: "
    user_input = input(display_prompt).strip()
    return user_input if user_input else default_value


class AmbiguityCheckResponse(BaseModel):
    clarity: str
    clarifying_question: str


def check_ambiguity_until_clear(
    user_question: str, db: str, chat_history: List[Dict]
) -> Tuple[str, AmbiguityCheckResponse, List[Dict]]:
    """
    Iteratively check for ambiguity and guide the user to clarify until a clear, relevant question is obtained.
    Returns the clarified question, the final LLM response, and the updated chat history.
    """
    while True:
        ambiguity_prompt = generate_prompt(
            DATASET_PATH, user_question, db, AMBIGUITY_PROMPT
        )
        ambiguity_llm_response: AmbiguityCheckResponse = get_query_response(
            prompt=ambiguity_prompt,
            model_name="gpt-4.1-mini",
            mode="structured",
            text_format=AmbiguityCheckResponse,
        )
        print("\n[Ambiguity Check] LLM Response:", ambiguity_llm_response)

        clarity_status = ambiguity_llm_response.clarity.strip().lower()
        if clarity_status == "clear":
            break
        elif clarity_status == "unrelated":
            print(
                "⚠️  Your question was detected as unrelated to the database. Please enter a relevant question."
            )
            user_question = get_user_input("Re-enter question", user_question)
            # Don't append this to chat_history—question was not relevant.
        elif clarity_status == "not clear":
            print(
                "⚠️  Ambiguous input detected. Model suggests clarification is needed."
            )
            if ambiguity_llm_response.clarifying_question:
                print(
                    f"Clarifying Question: {ambiguity_llm_response.clarifying_question}"
                )
            clarification = get_user_input("Please clarify", user_question)
            chat_history.append({"role": "user", "content": clarification})
            question_and_clarifications = user_question
            if clarification and clarification != user_question:
                question_and_clarifications += "\n" + clarification
            summarization_prompt = generate_prompt(
                DATASET_PATH,
                question_and_clarifications,
                db,
                SUMMARIZE_CLARIFICATIONS_PROMPT,
            )
            summary = get_query_response(
                prompt=summarization_prompt,
                model_name="gpt-4.1-mini",
                mode="chat",
            )
            print(f"[Summary after clarification] {summary}")
            user_question = summary
        else:
            print(
                f"⚠️  Unexpected clarity status from LLM: '{clarity_status}'. Review required."
            )
            break
    return user_question, ambiguity_llm_response, chat_history


def main():
    print("=" * 60)
    print("  Conversational Text2SQL Pipeline")
    print("=" * 60)
    # Defaults (override by prompting, but fallback to defaults in non-interactive)
    default_question = """I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."""

    default_db = "exchange_traded_funds"

    try:
        question = get_user_input("Enter Question", default_question)
        db = get_user_input("Enter Database name", default_db)
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Exiting.")
        sys.exit(1)
    # Chat history helps provide continuity if multiple clarifications occur
    chat_history: List[Dict] = []

    # Step 1: Ambiguity Resolution
    question, ambiguity_llm_response, chat_history = check_ambiguity_until_clear(
        question, db, chat_history
    )
    print("\n[After Ambiguity Resolution]")
    print("Final user question:", question)
    print("LLM Ambiguity Response:", ambiguity_llm_response)
    print("Chat History:", chat_history)

    # Step 2: Generate SQL with clarified question
    db_schema_inputs = get_db_schema_and_metadata(
        DATASET_PATH=DATASET_PATH,
        db=db,
    )
    db_schema_inputs["user_question"] = question

    print("\n[SQL Generation]")
    response = ConversationalText2SQLCrew().crew().kickoff(inputs=db_schema_inputs)
    if hasattr(response, "pydantic") and hasattr(response.pydantic, "df_output"):
        parsed_sql_output = pd.DataFrame(response.pydantic.df_output)
        print(parsed_sql_output)
    else:
        print("No SQL output was returned.")


if __name__ == "__main__":
    main()
