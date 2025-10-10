import streamlit as st
from conversational_txt2sql.main_pipeline import extract_sql_from_response
from conversational_txt2sql.prompt import generate_prompt
from conversational_txt2sql.call_api import get_query_response
import time
from conversational_txt2sql import get_config
import pandas as pd
from conversational_txt2sql.database_utils import execute_sql_query

CONFIGS = get_config()
DEFAULT_DB_CONFIG = CONFIGS["DEFAULT_DB_CONFIG"]
DATASET_PATH = CONFIGS["DATASET_PATH"]


def main():
    # Fancy background CSS
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        }
        .stApp {
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
        }
        .fancy-title {
            font-size: 2.8em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.2em;
            color: #2d3e50;
            text-shadow: 2px 2px 8px #fff, 0 0 2px #66a6ff;
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

    if st.button("Generate SQL Query"):
        prompt = generate_prompt(DATASET_PATH, question, db)
        # Fancy spinner while processing
        with st.spinner(
            "✨ Crunching your question and talking to the tables... Please wait! 🚀"
        ):
            start_time = time.time()
            llm_response = get_query_response(prompt=prompt, model_name="gpt-4.1-mini")
            elapsed = time.time() - start_time
            sql_query = extract_sql_from_response(llm_response)
        if sql_query:
            st.markdown("#### Generated SQL Query")
            st.code(sql_query, language="sql")
            st.markdown(
                f'<div style="color:white;font-size:1.1em;font-weight:bold;">⏱️ Response time: {elapsed:.2f} seconds</div>',
                unsafe_allow_html=True,
            )
            # QUERY the database and show results as DataFrame
            with st.spinner("Running query on database..."):
                results = execute_sql_query(sql_query, db, db_config=DEFAULT_DB_CONFIG)
                if not results.empty:
                    st.markdown("#### SQL Query Results")
                    st.dataframe(results)
                else:
                    st.warning("No results returned or query failed.")
        else:
            st.error("No SQL query found in the LLM response.")
            st.markdown(
                f'<div style="color:white;font-size:1.1em;font-weight:bold;">⏱️ Response time: {elapsed:.2f} seconds</div>',
                unsafe_allow_html=True,
            )


# Run the app
if __name__ == "__main__":
    main()
