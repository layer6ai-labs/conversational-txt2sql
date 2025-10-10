from conversational_txt2sql.call_api import get_query_response
from conversational_txt2sql.prompt import generate_prompt
from conversational_txt2sql.evaluation import llm_judge
from conversational_txt2sql.utils import execute_sql_query, initialize_database
import re
import os


# DUMP_FOLDER = "data/bird-interact-full-dumps"
DATASET_PATH = "data/table_schema_info"

def get_user_input(prompt: str, default_value: str = "") -> str:
    """
    Get user input with a default value.

    Args:
        prompt: The prompt to display to the user
        default_value: The default value to use if user enters nothing

    Returns:
        User input if provided, otherwise the default value
    """
    if default_value:
        display_prompt = f"{prompt} (default: '{default_value[:50]}{'...' if len(default_value) > 50 else ''}'): "
    else:
        display_prompt = f"{prompt}: "

    user_input = input(display_prompt).strip()
    return user_input if user_input else default_value


def extract_sql_from_response(response: str) -> str:
    """
    Extracts the SQL query from the LLM response between <SQL> and </SQL> tags.

    Args:
        response: The response string from the LLM.

    Returns:
        The extracted SQL query, stripped of leading/trailing whitespace.
        Returns an empty string if no SQL tags are found.
    """
    match = re.search(r"<SQL>(.*?)</SQL>", response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def main():
    """Main function to run the text-to-SQL evaluation pipeline."""
    # Step 1: Get the input question and database context with defaults
    default_question = "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
    default_db = "exchange_traded_funds"

    # Get user input with default values
    question = get_user_input("Enter Question: ", default_question)
    db = get_user_input("Enter Database name: ", default_db)

    # Step 2: Create a prompt for the LLM
    prompt = generate_prompt(DATASET_PATH, question, db)
    print("Step 2: Generated Prompt:")
    print(prompt)

    # Step 3: Get the response from the LLM
    llm_response = get_query_response(prompt=prompt, model_name="gpt-4.1-mini")
    print("Step 3: LLM Response:")
    print(llm_response)
    
    # NOT REQUIRED: Because we are doing this on initialization of postgres container
    # initialize_database(DUMP_FOLDER, db)

    # Step 4: Extract the SQL query from the LLM's response
    predicted_sql_query = extract_sql_from_response(llm_response)
    print("Step 4: Extracted SQL Query:")
    print(predicted_sql_query)
    if not predicted_sql_query:
        print("No SQL query found in the LLM response.")
        return

    predicted_sql_query = "WITH BondQuality AS (\n    SELECT\n        fundlink,\n        SUM(ba.allocationpct) FILTER (WHERE br.creditmark IN ('us_government', 'aaa', 'aa')) AS high_quality_alloc\n    FROM\n        bond_allocations ba\n    INNER JOIN\n        bond_ratings br ON ba.ratinglink = br.ratekey\n    GROUP BY\n        fundlink\n),\nFundRatios AS (\n    SELECT\n        tickersym,\n        shortlabel,\n        -- The NULLIF function prevents division-by-zero errors if the net expense is 0.\n        (fundmetrics ->> 'Yield_Rate')::numeric / NULLIF((fundmetrics ->> 'Expense_Net')::numeric, 0) AS yter\n    FROM\n        funds\n    WHERE\n        (fundmetrics ->> 'Yield_Rate')::numeric > 0\n)\nSELECT\n    f.tickersym,\n    f.shortlabel,\n    -- The RANK() window function assigns a rank to each fund based on its final score.\n    RANK() OVER (ORDER BY (fr.yter * bq.high_quality_alloc) DESC) AS premier_rank,\n    (fr.yter * bq.high_quality_alloc) AS secure_income_score\nFROM\n    funds f\nINNER JOIN\n    FundRatios fr ON f.tickersym = fr.tickersym\nINNER JOIN\n    BondQuality bq ON f.tickersym = bq.fundlink\nWHERE\n    fr.yter > 15 AND bq.high_quality_alloc > 0.6\nORDER BY\n    premier_rank;"  # Example SQL query for testing
    # Step 5: Execute the predicted SQL query to get its results
    print("Step 5a: Executing the predicted SQL query...")
    predicted_results = execute_sql_query(predicted_sql_query, db)
    print("\n\nStep 5b: Predicted SQL Query Results:")
    print(predicted_results)

    # # Step 6: Get and execute the ground truth SQL query for comparison
    # ground_truth_query = get_ground_truth_query(question, db)
    # ground_truth_results = execute_sql_query(ground_truth_query, db)

    # # Step 7: Compare the queries: Generated SQL and Ground Truth SQL

    # comparison = llm_judge(predicted_sql_query, ground_truth_query)

    # # Step 8: Compare the results and print the evaluation
    # evaluation_outcome = evaluate_results(predicted_results, ground_truth_results)
    # print("\n--- FINAL RESULT ---")
    # print(evaluation_outcome)


if __name__ == "__main__":
    main()
