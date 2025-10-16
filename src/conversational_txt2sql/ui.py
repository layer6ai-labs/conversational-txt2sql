import streamlit as st
import pandas as pd
from pydantic import BaseModel
from conversational_txt2sql.prompt import generate_prompt, get_db_schema_and_metadata, AMBIGUITY_PROMPT
from conversational_txt2sql.call_api import get_query_response
from conversational_txt2sql.agentic.crew import ConversationalText2SQLCrew
import os

# Configs
DATASET_PATH = "data/table_schema_info"
DEFAULT_DB = "exchange_traded_funds"

class AmbiguityCheckResponse(BaseModel):
    clarity: str
    clarifying_question: str

def main():
    # ---- UI Styling & Title ----
    st.set_page_config("Conversational Text2SQL Pipeline", page_icon="🦾", layout="wide")
    st.markdown("<h2 style='color:#247D24;text-align:center;'>Conversational Text2SQL Pipeline 🗣️📊🦾</h2>", unsafe_allow_html=True)

    # ---- Sidebar: Conversation History & Reset ----
    with st.sidebar:
        st.markdown("### Conversation History")
        if "conversation_history" in st.session_state and st.session_state["conversation_history"]:
            for i, q in enumerate(st.session_state["conversation_history"], 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.info("No conversation yet.")
        if st.button("Clear All / Start New"):
            for k in [
                "conversation_history","clarity_status","clarification_pending","ambiguity_llm_response","final_question","result_df","result_ready"]:
                st.session_state.pop(k, None)
            st.rerun()

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
    if "result_ready" not in st.session_state:
        st.session_state["result_ready"] = False
    if "result_df" not in st.session_state:
        st.session_state["result_df"] = None

    # ---- Main Input Form ----
    with st.form("question_form"):
        default_question = "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
        question = st.text_area("Enter your question:", value=st.session_state["final_question"] or default_question, height=120)
        db = st.selectbox("Select database:", [DEFAULT_DB])
        submit = st.form_submit_button("Submit")

    # ---- Clarification Input ----
    clarification = ""
    awaiting_clarification = (
        st.session_state["clarity_status"] == "not clear" or st.session_state["clarification_pending"]
    )
    if awaiting_clarification:
        st.warning("⚠️  Ambiguous input detected. Please clarify your question.")
        ambiguity_llm_response = st.session_state["ambiguity_llm_response"]
        clarifying_q = ambiguity_llm_response.clarifying_question if ambiguity_llm_response else "Clarifying question needed."
        clarification = st.text_input(clarifying_q)
        if st.button("Submit Clarification"):
            if not clarification.strip():
                st.error("Please provide a clarification.")
            else:
                st.session_state["conversation_history"].append(f"Clarification: {clarification}")
                # Update question with clarification (summarize if desired)
                question_and_clarification = st.session_state["final_question"] + "\n" + clarification
                # Re-run ambiguity prompt
                ambiguity_prompt = generate_prompt(DATASET_PATH, question_and_clarification, db, AMBIGUITY_PROMPT)
                ambiguity_llm_response = get_query_response(
                    prompt=ambiguity_prompt,
                    model_name="gpt-4.1-mini",
                    mode="structured",
                    text_format=AmbiguityCheckResponse,
                )
                clarity_status = ambiguity_llm_response.clarity.strip().lower()
                st.session_state["clarity_status"] = clarity_status
                st.session_state["ambiguity_llm_response"] = ambiguity_llm_response
                st.session_state["clarification_pending"] = (clarity_status == "not clear")
                if clarity_status == "unrelated":
                    st.session_state["conversation_history"] = []
                    st.session_state["final_question"] = ""
                    st.error("❌ The entered question was detected as unrelated to the database. Please enter a relevant question.")
                    st.session_state["clarification_pending"] = False
                elif clarity_status == "clear":
                    st.session_state["final_question"] = question_and_clarification
                st.rerun()

    # ---- Initial Submission and Ambiguity Checking ----
    elif submit and question.strip():
        # Only allow new question submission if not in the clarification loop
        st.session_state["conversation_history"].append(f"Question: {question.strip()}")
        ambiguity_prompt = generate_prompt(DATASET_PATH, question.strip(), db, AMBIGUITY_PROMPT)
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
        st.session_state["clarification_pending"] = (clarity_status == "not clear")
        if clarity_status == "unrelated":
            st.session_state["conversation_history"] = []
            st.session_state["final_question"] = ""
            st.error("❌ The entered question was detected as unrelated to the database. Please enter a relevant question.")
            st.session_state["clarification_pending"] = False
        st.rerun()

    # ---- When question is CLEAR: Generate and Show Results ----
    if st.session_state["clarity_status"] == "clear" and not st.session_state["clarification_pending"]:
        st.success("✅ Question is clear! Generating SQL and running... This may take a moment.")
        db_schema_inputs = get_db_schema_and_metadata(DATASET_PATH=DATASET_PATH, db=db)
        db_schema_inputs["user_question"] = st.session_state["final_question"]
        with st.spinner("Running Text2SQL agent and collecting results..."):
            response = ConversationalText2SQLCrew().crew().kickoff(inputs=db_schema_inputs)
        # Expect DataFrameOutputModel-like output, convert to DataFrame:
        df = None
        if hasattr(response, "pydantic") and hasattr(response.pydantic, "df_output"):
            try:
                df = pd.DataFrame(response.pydantic.df_output)
            except Exception as ex:
                st.error(f"Result conversion failed: {ex}")
        st.session_state["result_df"] = df
        st.session_state["result_ready"] = df is not None and not df.empty
        # st.rerun()

    # ---- Display output if available ----
    if st.session_state.get("result_ready"):
        st.subheader("Results table:")
        st.dataframe(st.session_state["result_df"])
        csv = st.session_state["result_df"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
        )
    elif st.session_state.get("result_ready") is False and st.session_state.get("clarity_status") == "clear":
        st.info("No SQL output was returned.")

    # ---- End ----

if __name__ == "__main__":
    main()
