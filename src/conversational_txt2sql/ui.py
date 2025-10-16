import streamlit as st
from conversational_txt2sql.prompt import generate_prompt
from conversational_txt2sql.call_api import get_query_response
import time
from conversational_txt2sql import get_config
import pandas as pd
from conversational_txt2sql.database_utils import execute_sql_query
import sys
from typing import List, Dict, Tuple

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

CONFIGS = get_config()
DEFAULT_DB_CONFIG = CONFIGS["DEFAULT_DB_CONFIG"]
DATASET_PATH = CONFIGS["DATASET_PATH"]

class AmbiguityCheckResponse(BaseModel):
    clarity: str
    clarifying_question: str


def main():
    # Fancy background CSS
    st.markdown(
        """
        <style>
        body, .stApp {
            background: #247D24 !important;
        }
        .logo-container {
            position: fixed;
            top: 100px;
            left: 22px;
            z-index: 9999;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 8px #3c763d20;
            padding: 8px 14px 8px 8px;
            height: 60px;
            display: flex;
            align-items: center;
        }
        .logo-img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }
        .fancy-title {
            font-size: 2.8em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.2em;
            color: #94C29F;
            
        }
        .sql-output {
            background: #fff;
            border-radius: 10px;
            padding: 1em;
            box-shadow: 0 2px 8px rgba(102,166,255,0.15);
            font-size: 1.2em;
            color: #222;
            margin-top: 1em;
        }
        </style>
        </div>
        </div>
        <div class="logo-container">
            <img src="https://www.bing.com/th/id/OIP.aiBQQPej85d133DWLzJcpwHaEK?w=327&h=211&c=8&rs=1&qlt=90&o=6&cb=12&dpr=1.3&pid=3.1&rm=2" class="logo-img" alt="TD Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="fancy-title">TALK WITH YOUR TABLES !! 🗣️📊🦾</div>',
        unsafe_allow_html=True,
    )

    default_question = "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
    db_options = ["exchange_traded_funds"]

    question = st.text_area("Enter Question:", value=default_question, height=120)
    db = st.selectbox("Enter Database name:", db_options)
    # --------- REWRITTEN LOGIC STARTS HERE ---------
    
    # Initialize conversation history in Streamlit session state
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = []

    # Ambiguity simulation logic replaced -- check clarity status, and conditionally branch
    import random
    
    if "clarity_status" not in st.session_state:
        st.session_state["clarity_status"] = None
        st.session_state["awaiting_clarification"] = False

    unrelated_warning = None  # Track unrelated scenario flag/message

    # The possible entry points of the interface:
    # 1. User is clarifying a question
    # 2. User is asking a new question (pressed Submit Question)
    # 3. User needs to be notified of unrelated/unhandled statuses

    if st.session_state.get("clarity_status") == "not clear" or st.session_state.get("awaiting_clarification", False):
        st.warning("⚠️  Ambiguous input detected. Please clarify your question so we can proceed.")
        clarification = st.text_input("Please provide a clarification for your previous question:")
        if st.button("Enter Clarifying Question"):
            if clarification:
                st.session_state["conversation_history"].append(f"Clarification: {clarification}")
                st.success(f"**Clarification entered:** {clarification}")
                # After clarification, simulate that the question is now clear
                st.session_state["clarity_status"] = "clear"
                st.session_state["awaiting_clarification"] = False
                st.rerun()
            else:
                st.error("Please enter a clarification before submitting.")
        else:
            st.session_state["awaiting_clarification"] = True

    elif st.session_state.get("clarity_status") == "unrelated":
        if not st.session_state.get("show_unrelated_warning", False):
            st.session_state["show_unrelated_warning"] = True
            st.session_state["conversation_history"] = []
            st.session_state["awaiting_clarification"] = False
            st.rerun()
        unrelated_warning = "❌ The entered question was detected as unrelated to the database. Conversation history has been cleared. Please enter a relevant question."

    elif st.session_state.get("clarity_status") == "clear":
        # Run further logic for "clear" status here, currently stub
        st.markdown(
            '<span style="color: #b0b0b0;">✅ Question is clear.</span>', unsafe_allow_html=True
        )
        # Prepare for additional tasks below ("further logic" placeholder)
        # Example: Show next options, allow for SQL generation, etc.
        # (No-op for now; this area can later receive SQL query/output handling, etc.)

        # Optionally show last question entered
        if st.session_state["conversation_history"]:
            st.markdown(f"**Last question:** {st.session_state['conversation_history'][-1]}")

    else:
        if st.button("Submit Question"):
            # Store the entered question in conversation history
            st.session_state["conversation_history"].append(question)
            st.markdown(f'<span style="color: black;">**You asked:** {question}</span>', unsafe_allow_html=True)

            # Simulate an ambiguity check result (replace with real LLM integration)
            st.session_state["clarity_status"] = random.choice(["clear", "unrelated", "not clear"])
            if st.session_state["clarity_status"] == "not clear":
                st.session_state["awaiting_clarification"] = True
                st.rerun()
            elif st.session_state["clarity_status"] == "unrelated":
                st.session_state["conversation_history"] = []
                st.session_state["awaiting_clarification"] = False
                st.session_state["show_unrelated_warning"] = True
                st.session_state["clarity_status"] = None  # Allow resubmission after unrelated warning
                # Do NOT rerun here; instead, let the code flow continue to display Submit/Clear buttons
            else:
                st.session_state["awaiting_clarification"] = False
                st.rerun()

    # Show unrelated warning if set from rerun context
    if st.session_state.get("show_unrelated_warning", False):
        st.markdown(
            '<div style="color: #b41c1c; solid #ffeeba; '
            'padding: 16px; border-radius: 6px; font-size: 1.08em;">'
            '❌ <b>The entered question was detected as unrelated to the database. Conversation history has been cleared. Please enter a relevant question.</b>'
            '</div>', unsafe_allow_html=True
        )
        st.session_state["show_unrelated_warning"] = False

    # Display conversation history in the sidebar
    with st.sidebar:
        st.markdown("### Conversation History")
        if st.session_state["conversation_history"]:
            for i, q in enumerate(st.session_state["conversation_history"], 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.info("No questions yet.")

    # Add a button to clear conversation history
    if st.button("Clear Conversation History"):
        st.session_state["conversation_history"] = []
        st.success("Conversation history cleared.")
        st.session_state["clarity_status"] = None
        st.session_state["awaiting_clarification"] = False
        st.rerun()

if __name__ == "__main__":
    main()
