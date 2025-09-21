from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class Conditions(BaseModel):
    """
    'conditions': {'decimal': 4, 'distinct': False, 'order': False}, 
    """
    decimal: int
    distinct: bool
    order: bool

class UserQueryAmbiguityItem(BaseModel):
    """
    {
        'term': 'downtime score', 
        'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
        'is_mask': True, 
        'type': 'knowledge_linking_ambiguity'
    }
    """
    term: str
    sql_snippet: str
    is_mask: bool
    type: str

class UserQueryAmbiguity(BaseModel):
    """
    'user_query_ambiguity': {
        'critical_ambiguity': [
            {
                'term': 'downtime score', 
                'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
                'is_mask': True, 
                'type': 'knowledge_linking_ambiguity'
            }, 
            {
                'term': 'down', 
                'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
                'is_mask': True, 
                'type': 'semantic_ambiguity'
            }
        ], 
        'non_critical_ambiguity': [
            {
                'term': 'rounded', 
                'sql_snippet': 'ROUND(CAST(om."mttrh" / (om."mtbfh" + om."mttrh") AS numeric), 4)', 
                'is_mask': False, 
                'type': 'decimal_ambiguity'
            }
        ]
    },
    """
    critical_ambiguity: list[UserQueryAmbiguityItem]
    non_critical_ambiguity: list[UserQueryAmbiguityItem]

class KnowledgeAmbiguityItem(BaseModel):
    """
    {
        'term': 'System Unavailability', 
        'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
        'is_mask': True, 
        'type': 'knowledge_ambiguity', 
        'deleted_knowledge': 4
    }
    """
    term: str
    sql_snippet: str
    is_mask: bool
    type: str
    deleted_knowledge: int

class FollowUp(BaseModel):
    """
    'follow_up': {
        'query': "Now, calculate the difference between the System Unavailability for 'Solar Plant West Davidport' and the average System Unavailability across all other plants where the necessary data (MTBF and MTTR) is available.\nPresent the result as a single numeric value, rounded to 4 decimal places.", 
        'sol_sql': [], 
        'external_knowledge': [], 
        'type': 'topic_pivot', 
        'category': 'Query', 
        'test_cases': [], 
        'conditions': {'decimal': 4, 'distinct': False, 'order': False}, 
        'output_type': 'scalar'
    }
    """
    query: str
    sol_sql: list[str]
    external_knowledge: list[int]
    type: str
    category: str
    test_cases: list[str]
    conditions: Conditions
    output_type: Optional[str] = None  # sometimes missing

class Data(BaseModel):
    """
    {'instance_id': 'solar_panel_1', 
    'selected_database': 'solar_panel', 
    'preprocess_sql': [], 
    'clean_up_sqls': [], 
    'sol_sql': ['SELECT ROUND(CAST(om."mttrh" / (om."mtbfh" + om."mttrh") AS numeric), 4)\nFROM operational_metrics om\nJOIN plant_record pr ON om."snapops" = pr."snapkey"\nJOIN plants p ON pr."sitetie" = p."sitekey"\nWHERE LOWER(p."sitelabel") = \'solar plant west davidport\'\nLIMIT 1;'], 
    'external_knowledge': [4], 
    'test_cases': [], 
    'high_level': False, 
    'category': 'Query', 
    'conditions': {'decimal': 4, 'distinct': False, 'order': False}, 
    'output_type': 'scalar', 
    'amb_user_query': "What's the downtime score for 'Solar Plant West Davidport'?", 
    'user_query_ambiguity': {
        'critical_ambiguity': [
            {
                'term': 'downtime score', 
                'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
                'is_mask': True, 
                'type': 'knowledge_linking_ambiguity'
            }, 
            {
                'term': 'down', 
                'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
                'is_mask': True, 
                'type': 'semantic_ambiguity'
            }
        ], 
        'non_critical_ambiguity': [
            {
                'term': 'rounded', 
                'sql_snippet': 'ROUND(CAST(om."mttrh" / (om."mtbfh" + om."mttrh") AS numeric), 4)', 
                'is_mask': False, 
                'type': 'decimal_ambiguity'
            }
        ]
    },
    'knowledge_ambiguity': [{
        'term': 'System Unavailability', 
        'sql_snippet': 'om."mttrh" / (om."mtbfh" + om."mttrh")', 
        'is_mask': True, 
        'type': 'knowledge_ambiguity', 
        'deleted_knowledge': 4
    }],
    'follow_up': {
        'query': "Now, calculate the difference between the System Unavailability for 'Solar Plant West Davidport' and the average System Unavailability across all other plants where the necessary data (MTBF and MTTR) is available.\nPresent the result as a single numeric value, rounded to 4 decimal places.", 
        'sol_sql': [], 
        'external_knowledge': [], 
        'type': 'topic_pivot', 
        'category': 'Query', 
        'test_cases': [], 
        'conditions': {'decimal': 4, 'distinct': False, 'order': False}, 
        'output_type': 'scalar'
    }
    """
    instance_id: str
    selected_database: str
    preprocess_sql: list[str]
    clean_up_sqls: list[str]
    sol_sql: list[str]
    external_knowledge: list[int]
    test_cases: list[str]
    high_level: bool
    category: str
    output_type: Optional[str] = None  # sometimes missing
    amb_user_query: str