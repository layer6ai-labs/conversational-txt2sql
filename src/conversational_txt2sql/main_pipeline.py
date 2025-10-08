from conversational_txt2sql.call_api import get_query_response
from conversational_txt2sql.prompt import generate_prompt


def main():
    """Main function to run the text-to-SQL evaluation pipeline."""
    # Step 1: Get the input question and database context
    # question, db = `get_user_question_and_db()
    question = "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."
    db = "exchange_traded_funds"
    # Step 2: Create a prompt for the LLM
    prompt = generate_prompt(question, db)
    print("Step 2: Generated Prompt:")
    print(prompt)
    prompt = "I need to find the top-performing income funds for a client. Could you please identify all the premium funds available? For each one, calculate its secure income efficiency score. Please show me the fund's ticker symbol, its name, and its score."

    # Step 3: Get the response from the LLM
    llm_response = get_query_response(prompt=prompt, model_name="gpt-4.1-mini")
    
    # Step 4: Extract the SQL query from the LLM's response
    predicted_sql_query = extract_sql_from_response(llm_response)

    # Step 5: Execute the predicted SQL query to get its results
    print("Step 5a: Executing the predicted SQL query...")
    predicted_results = execute_sql_query(predicted_sql_query, db)

    # Step 6: Get and execute the ground truth SQL query for comparison
    ground_truth_query = get_ground_truth_query(question, db)
    ground_truth_results = execute_sql_query(ground_truth_query, db)

    # Step 7: Compare the results and print the evaluation
    evaluation_outcome = evaluate_results(predicted_results, ground_truth_results)
    print("\n--- FINAL RESULT ---")
    print(evaluation_outcome)


if __name__ == "__main__":
    main()
