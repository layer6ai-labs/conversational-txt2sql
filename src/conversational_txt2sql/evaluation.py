"""
Structured Output reference :
https://platform.openai.com/docs/guides/structured-outputs?example=chain-of-thought
"""

# %%
from pydantic import BaseModel

from conversational_txt2sql.call_api import get_query_response


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


def llm_judge(sql1, sql2, model_name="gpt-4.1-mini"):
    prompt = f"""
    You are a senior SQL architect and evaluator. Your assignment is to conduct a meticulous, expert-level comparison of the two SQL queries provided below, assessing their logical equivalence and functional parity. Your analysis should be comprehensive, impartial, and based on the following advanced criteria.

    === Advanced Comparison Criteria ===
    1. SELECT Clause:
       - Determine if both queries select an equivalent set of columns, regardless of order, aliasing, or naming conventions.
       - Resolve all table and column aliases to their canonical names.
       - Assess equivalence of derived columns, expressions, and aggregate functions, including their logic and computation.
       - Consider the impact of DISTINCT, aggregate functions, and any column-level transformations.

    2. FROM Clause:
       - Verify that both queries reference the same tables and establish equivalent JOIN relationships.
       - For INNER JOINs, table order is not significant; for OUTER JOINs (LEFT, RIGHT, FULL), ensure join direction and table order are preserved.
       - Resolve all table aliases and ensure join conditions are logically equivalent, including multi-table and nested joins.
       - Account for the presence of subqueries or derived tables in the FROM clause.

    3. WHERE Clause:
       - Confirm that both queries apply logically equivalent filtering conditions, regardless of order or formatting.
       - Resolve all references to table and column aliases.
       - Consider logical equivalence of predicates, including AND/OR combinations, predicate order, and use of functions or expressions.

    4. HAVING Clause:
       - Ensure both queries apply equivalent aggregate filtering conditions.
       - Resolve references to aliases and derived columns.
       - Assess logical equivalence, not just syntactic similarity.

    5. GROUP BY Clause:
       - Verify that both queries group by an equivalent set of columns.
       - If numeric indices are used, map them to the corresponding columns in the SELECT statement before comparison.
       - Resolve all aliases and ensure logical equivalence, including the impact on aggregation.

    6. Common Table Expressions (CTEs):
       - If either query uses CTEs (WITH ... AS), compare their definitions for logical and functional equivalence.
       - Ensure consistent referencing and usage of CTEs in the main query.
       - Resolve all nested CTEs and subqueries, and assess their impact on the overall query logic.

    7. Subqueries:
       - Assess the presence and structure of subqueries in any clause (SELECT, FROM, WHERE, HAVING).
       - Ensure logical equivalence of subquery logic, filtering, and correlation with parent queries.
       - Consider the use of EXISTS, IN, and other subquery constructs, ensuring functional parity.

    8. Additional Considerations:
       - Account for differences in formatting, whitespace, or case sensitivity that do not affect logical structure.
       - Consider the impact of database-specific functions, features, or syntax.
       - Evaluate the use of window functions, set operations (UNION, INTERSECT, EXCEPT), and other advanced SQL constructs.

    === Instructions ===
    - Extract and normalize the SELECT, FROM, WHERE, HAVING, GROUP BY clauses, and any CTEs from both queries.
    - Resolve all table and column aliases to their original names prior to comparison.
    - Focus on logical and functional equivalence, not mere syntactic similarity.
    - Provide detailed, professional reasoning and explanations for each clause comparison, highlighting any discrepancies or equivalences.
    - Return a structured response containing:
        1. A dictionary indicating whether each clause matches (True/False).
        2. Two dictionaries showing the extracted components from each SQL query, including CTE definitions if present.
        3. A dictionary providing detailed explanations for each clause comparison.
        4. A final answer stating whether the queries are logically equivalent overall, with clear justification.

    === SQL Queries for Comparison ===
    ###########
    Query 1:
    {sql1}

    ###########
    Query 2:
    {sql2}
    ###########
    """
    response = get_query_response(
        prompt=prompt,
        model_name=model_name,
        text_format=ComparisonReasoning,
        mode="structured",
    )
    return response


# %%

# # Example usage:
# sql_query1 = """
# SELECT table2.a, table2.b, SUM(table1.c)
# FROM table1
# JOIN table2 ON table1.id = table2.t1_id
# WHERE table2.a > 10 AND table2.b < 20
# GROUP BY table2.a, table2.b
# HAVING SUM(table1.c) > 100
# """
# sql_query2 = """
# SELECT a, b, SUM(c)
# FROM table2
# JOIN table1 ON table1.id = table2.t1_id
# WHERE b < 20 AND a > 10
# GROUP BY 2,1
# HAVING SUM(c) > 100
# """

# sql_query3 = """
# WITH joined_tables AS (
#     SELECT a1.a as a, a1.b as b, a2.c as c
#     FROM table2 as a1
#     JOIN table1 as a2 ON a2.id = a1.t1_id
# )
# SELECT a, b, SUM(c)
# FROM joined_tables
# WHERE b < 20 AND a > 10
# GROUP BY b, a
# HAVING SUM(c) > 100
# """

# result = llm_judge(sql_query1, sql_query3)

# print(result)
# %%
