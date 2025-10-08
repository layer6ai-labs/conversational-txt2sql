
def main():
    """Main function to run the text-to-SQL evaluation pipeline."""
    # Step 1: Get the input question and database context
    question, db_context = get_user_question_and_db_context()

    # Step 2: Create a prompt for the LLM
    prompt = generate_text_to_sql_prompt(question, db_context)

    # Step 3: Get the response from the LLM
    llm_response = query_language_model(prompt)

    # Step 4: Extract the SQL query from the LLM's response
    predicted_sql_query = extract_sql_from_response(llm_response)

    # Step 5: Execute the predicted SQL query to get its results
    print("Step 5a: Executing the predicted SQL query...")
    predicted_results = execute_sql_query(predicted_sql_query, db_context)

    # Step 6: Get and execute the ground truth SQL query for comparison
    ground_truth_query = get_ground_truth_query(db_context)
    ground_truth_results = execute_sql_query(ground_truth_query, db_context)

    # Step 7: Compare the results and print the evaluation
    evaluation_outcome = evaluate_results(predicted_results, ground_truth_results)
    print("\n--- FINAL RESULT ---")
    print(evaluation_outcome)


if __name__ == "__main__":
    main()
