from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
