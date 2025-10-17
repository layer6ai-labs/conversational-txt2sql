import os
import pandas as pd
import streamlit as st
from pydantic import BaseModel

from conversational_txt2sql.agentic.naive_crew import ConversationalText2SQLCrew
from conversational_txt2sql.call_api import get_query_response
from conversational_txt2sql.prompt import (
    AMBIGUITY_PROMPT,
    generate_prompt,
    get_db_schema_and_metadata,
)

# Configs
DATASET_PATH = "data/table_schema_info"
DEFAULT_DB = "exchange_traded_funds"


class AmbiguityCheckResponse(BaseModel):
    clarity: str
    clarifying_question: str


def main():
    # ---- UI Styling & Title ----
    st.set_page_config(
        "Conversational Text2SQL Pipeline", page_icon="🦾", layout="wide"
    )
    st.markdown(
        "<h2 style='color:#247D24;text-align:center;'>Conversational Text2SQL Pipeline 🗣️📊🦾</h2>",
        unsafe_allow_html=True,
    )

    # ---- Sidebar: Clear Button & History ----
    with st.sidebar:
        if st.button("Clear All / Start New"):
            for k in st.session_state.keys():
                del st.session_state[k]
            st.rerun()
        st.markdown("### Conversation History")
        if "conversation_history" in st.session_state and st.session_state["conversation_history"]:
            for i, q in enumerate(st.session_state["conversation_history"], 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.info("No conversation yet.")

    # ---- Session State ----
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = []
    if "clarity_status" not in st.session_state:
        st.session_state["clarity_status"] = None
    if "ambiguity_llm_response" not in st.session_state:
        st.session_state["ambiguity_llm_response"] = None
    if "clarification_pending" not in st.session_state:
        st.session_state["clarification_pending"] = False
    if "final_question" not in st.session_state:
        st.session_state["final_question"] = ""
    if "turns" not in st.session_state:
        st.session_state["turns"] = []  # List of {"question": str, "result_df": pd.DataFrame}
    if "result_ready" not in st.session_state:
        st.session_state["result_ready"] = False
    if "result_df" not in st.session_state:
        st.session_state["result_df"] = None
    if "show_unrelated_error" not in st.session_state:
        st.session_state["show_unrelated_error"] = False

    # ---- Display all previous turns ----
    st.markdown("### 💬 Previous Questions & Results")
    if st.session_state["turns"]:
        for i, turn in enumerate(st.session_state["turns"]):
            with st.container():
                st.markdown(f"**Q{i+1}:** {turn['question']}")
                st.dataframe(turn["result_df"])
                csv = turn["result_df"].to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"⬇️ Download results for Q{i+1}",
                    data=csv,
                    file_name=f"query_results_{i+1}.csv",
                    mime="text/csv",
                    key=f"download_{i}"
                )
            st.markdown("---")
    else:
        st.info("No results yet.")

    default_question = "Show me the performance trend for AADR. For each year, calculate its outperformance, the prior year's number, and the change."
    # ---- Main Input Form for new / follow-up question ----
    with st.form("question_form"):
        question = st.text_area(
            "Enter your question:",
            value=st.session_state["final_question"] or default_question,
            height=120,
        )
        db = st.selectbox("Select database:", [DEFAULT_DB])
        submit = st.form_submit_button("Submit")

    # ---- Error display for unrelated ----
    if st.session_state.get("show_unrelated_error"):
        st.error(
            "❌ The entered question was detected as unrelated to the database. Please enter a relevant question."
        )
        st.session_state["show_unrelated_error"] = False

    # ---- Clarification Input ----
    clarification = ""
    awaiting_clarification = (
        st.session_state["clarity_status"] == "not clear"
        or st.session_state["clarification_pending"]
    )
    if awaiting_clarification:
        st.warning("⚠️  Ambiguous input detected. Please clarify your question.")
        ambiguity_llm_response = st.session_state["ambiguity_llm_response"]
        clarifying_q = (
            ambiguity_llm_response.clarifying_question
            if ambiguity_llm_response
            else "Clarifying question needed."
        )

        col1, col2 = st.columns([2, 1])  # two buttons side by side
        with col1:
            clarification = st.text_input(clarifying_q)
            submit_clarification = st.button("Submit Clarification")
        with col2:
            skip_clarification = st.button("No patience anymore, show results / bye!")

        if submit_clarification:
            if not clarification.strip():
                st.error("Please provide a clarification.")
            else:
                st.session_state["conversation_history"].append(
                    f"Clarification: {clarification}"
                )
                question_and_clarification = (
                    st.session_state["final_question"] + "\n" + clarification
                )
                # Re-run ambiguity prompt
                ambiguity_prompt = generate_prompt(
                    DATASET_PATH, question_and_clarification, db, AMBIGUITY_PROMPT
                )
                ambiguity_llm_response = get_query_response(
                    prompt=ambiguity_prompt,
                    model_name="gpt-4.1-mini",
                    mode="structured",
                    text_format=AmbiguityCheckResponse,
                )
                clarity_status = ambiguity_llm_response.clarity.strip().lower()
                st.session_state["clarity_status"] = clarity_status
                st.session_state["ambiguity_llm_response"] = ambiguity_llm_response
                st.session_state["clarification_pending"] = (
                    clarity_status == "not clear"
                )
                if clarity_status == "unrelated":
                    st.session_state["conversation_history"] = []
                    st.session_state["final_question"] = ""
                    st.session_state["clarification_pending"] = False
                    st.session_state["show_unrelated_error"] = True
                elif clarity_status == "clear":
                    st.session_state["final_question"] = question_and_clarification
                st.rerun()

        elif skip_clarification:
            # User chooses to bypass clarification → treat as clear
            st.session_state["clarity_status"] = "clear"
            st.session_state["clarification_pending"] = False
            st.session_state["final_question"] = st.session_state["final_question"]
            st.session_state["conversation_history"].append(
                f"Skipped clarification. Using question as-is."
            )
            st.rerun()
    # ---- Initial Submission and Ambiguity Checking ----
    elif submit and question.strip():
        st.session_state["conversation_history"].append(f"Question: {question.strip()}")
        ambiguity_prompt = generate_prompt(
            DATASET_PATH, question.strip(), db, AMBIGUITY_PROMPT
        )
        with st.spinner("Checking question clarity..."):
            ambiguity_llm_response = get_query_response(
                prompt=ambiguity_prompt,
                model_name="gpt-4.1-mini",
                mode="structured",
                text_format=AmbiguityCheckResponse,
            )
            clarity_status = ambiguity_llm_response.clarity.strip().lower()
        st.session_state["clarity_status"] = clarity_status
        st.session_state["ambiguity_llm_response"] = ambiguity_llm_response
        st.session_state["final_question"] = question.strip()
        st.session_state["clarification_pending"] = clarity_status == "not clear"
        if clarity_status == "unrelated":
            st.session_state["conversation_history"] = []
            st.session_state["final_question"] = ""
            st.session_state["clarification_pending"] = False
            st.session_state["show_unrelated_error"] = True
        st.rerun()

    # ---- When question is CLEAR: Generate and Show Results ----
    if (
        st.session_state["clarity_status"] == "clear"
        and not st.session_state["clarification_pending"]
    ):
        st.success(
            "✅ Question is clear! Generating SQL and running... This may take a moment."
        )
        db_schema_inputs = get_db_schema_and_metadata(DATASET_PATH=DATASET_PATH, db=db)
        db_schema_inputs["user_question"] = st.session_state["final_question"]
        with st.spinner("Running Text2SQL agent and collecting results..."):
            response = (
                ConversationalText2SQLCrew().crew().kickoff(inputs=db_schema_inputs)
            )
        df = None
        if hasattr(response, "pydantic") and hasattr(response.pydantic, "df_output"):
            try:
                df = pd.DataFrame(response.pydantic.df_output)
            except Exception as ex:
                st.error(f"Result conversion failed: {ex}")

        # ---- Append new turn instead of overwriting previous results ----
        st.session_state["turns"].append({
            "question": st.session_state["final_question"],
            "result_df": df
        })

        # ---- Reset for next question ----
        st.session_state["final_question"] = ""
        st.session_state["clarity_status"] = None
        st.session_state["clarification_pending"] = False
        st.session_state["ambiguity_llm_response"] = None
        st.session_state["result_ready"] = df is not None and not df.empty
        st.rerun()


if __name__ == "__main__":
    main()
