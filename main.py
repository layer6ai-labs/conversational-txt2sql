import os
from agents.sql_generator import SQLGenerator
from executors.sql_executor import SQLExecutor
from utils.data_loader import DataLoader

def main():
    print("Starting BIRD-Interact Agent Framework...")

    # 1. Load Data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    loader = DataLoader(base_path=current_dir)
    data_df = loader.load_csv("dummy_data.csv")

    if data_df.empty:
        print("Failed to load data. Exiting.")
        return

    # 2. Initialize Agents and Executors
    # In a more complex setup, schema_info would be dynamically extracted
    # or provided, possibly by another agent.
    schema_info = {
        "tables": {
            "dummy_table": {
                "columns": {"id": "int", "name": "text", "age": "int", "city": "text"}
            }
        }
    }
    sql_generator = SQLGenerator(schema_info=schema_info)
    sql_executor = SQLExecutor(data_df)

    # 3. Main Interaction Loop
    print("\nEnter your natural language queries (type 'exit' to quit):")
    while True:
        user_query = input("Query: ")
        if user_query.lower() == 'exit':
            break

        if not user_query.strip():
            print("Please enter a query.")
            continue

        # Generate SQL
        generated_sql = sql_generator.generate_sql(user_query)
        print(f"\nGenerated SQL:\n{generated_sql}")

        # Execute SQL
        execution_result_df = sql_executor.execute_sql(generated_sql)

        # Display Result
        print("\nExecution Result:")
        if not execution_result_df.empty:
            print(execution_result_df.to_string(index=False))
        else:
            print("No results or an error occurred during execution.")
        print("-" * 50)

    print("BIRD Agent Framework shutting down.")

if __name__ == "__main__":
    main()