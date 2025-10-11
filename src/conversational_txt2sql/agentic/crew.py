import os
from typing import Optional

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from conversational_txt2sql import get_config

# Custom Tool
from conversational_txt2sql.agentic.tools.database_tools import execute_sql_query_tool

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

llm = LLM(model=get_config()["MODEL"], api_key=OPENAI_API_KEY)


@CrewBase
class ConversationalText2SQLCrew:
    """
    Orchestrates a multi-agent crew for conversational Text-to-SQL translation.

    Responsibilities:
    - Converts natural language questions into executable SQL queries.
    - Executes generated SQL queries against the target database.
    - Collects, formats, and returns results or explanations to the end user.
    - Handles relevant database and conversational logic.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sql_generator(self) -> Agent:
        """
        Agent responsible for analyzing natural language questions and generating accurate, executable PostgreSQL SQL queries using provided schema details and knowledge bases.
        """
        return Agent(
            config=self.agents_config["sql_generator"],
            verbose=True,
            llm=llm,
        )

    @task
    def generate_sql(self) -> Task:
        """
        Task to generate a PostgreSQL SQL query from a complex natural language user question.

        This task leverages the SQL generator agent to analyze the question using the provided database schema, column meanings, and definitions.
        The output is an accurate, executable, and well-formatted SQL query that answers the user's intent, strictly grounded in the available schema knowledge.
        """
        return Task(config=self.tasks_config["generate_sql"])

    @crew
    def crew(self) -> Crew:
        """
        Defines and orchestrates the multi-agent crew for conversational Text-to-SQL translation using sequential task execution.
        """
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
