from pydantic import BaseModel

class State(BaseModel):
    """
    State used in langgraph node to store conversation history.
    """
    messages: list[str] = []