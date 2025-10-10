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
