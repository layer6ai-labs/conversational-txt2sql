#%%

from conversational_txt2sql.call_api import get_query_response
from pydantic import BaseModel

class Components(BaseModel):
    """Data model to hold extracted SQL components."""
    select_statement: str
    from_statement: str
    where_statement: str
    having_statement: str
    group_by_statement: str

class ComponentComparison(BaseModel):
    """Data model to hold comparison results for SQL components."""
    select_statement: bool
    from_statement: bool
    where_statement: bool
    having_statement: bool
    group_by_statement: bool

class ComponentComparisonExplanations(Components):
    """Data model to hold explanations for SQL component comparisons."""
    pass

class ComparisonReasoning(BaseModel):
    comparisons: ComponentComparison
    comparison_explanations: ComponentComparisonExplanations
    extracted_components_sql1: list[Components]
    extracted_components_sql2: list[Components]
    final_answer: str


def llm_judge(sql1, sql2,model_name="gpt-4.1-mini"):
    prompt = f"""
    You are a professional SQL evaluator. Your task is to rigorously compare the following two SQL queries for logical equivalence based on the criteria below:

    Comparison Criteria:
    1. SELECT clause: Both queries must select the same set of columns, regardless of order or aliasing.
    2. FROM clause: Both queries must reference the same tables and the same JOIN relationships.For INNER JOIN or JOIN, table order does not matter. For LEFT JOIN, RIGHT JOIN, FULL JOIN, or CROSS JOIN, table order must be preserved.
    4. WHERE clause: Both queries must apply the same filtering conditions, regardless of order.
    5. HAVING clause: Both queries must apply the same conditions, regardless of order.
    6. GROUP BY clause: Both queries must group by the same columns. If numeric indices are used, map them to the corresponding column in the SELECT statement before comparison.

    Instructions:
    - Only review the SELECT, FROM, WHERE, HAVING, and GROUP BY clauses.
    - Return three dictionaries:
        1. A dictionary indicating whether each clause matches (True/False).
        2. Two dictionaries showing the extracted components from each SQL query.

    Below are the two SQL queries for comparison:
    ###########
    Query 1:
    {sql1}

    ###########
    Query 2:
    {sql2}
    ###########
    """
    response = get_query_response(prompt=prompt, 
                                  model_name=model_name,
                                  text_format=ComparisonReasoning,
                                  mode="structured"
                                  )
    return response
# %%

# # Example usage:
# sql_query1 = """
# SELECT a, b, SUM(c)
# FROM table1
# JOIN table2 ON table1.id = table2.t1_id
# WHERE a > 10 AND b < 20
# GROUP BY a, b
# HAVING SUM(c) > 100
# """
# sql_query2 = """
# SELECT a, b, SUM(c)
# FROM table2
# JOIN table1 ON table1.id = table2.t1_id
# WHERE b < 20 AND a > 10
# GROUP BY 2,1
# HAVING SUM(c) > 100
# """

# result = llm_judge(sql_query1, sql_query2)

# print(result)
# %%
