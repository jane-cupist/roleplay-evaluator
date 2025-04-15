from typing import Annotated

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    age: int
    name: str


graph_builder = StateGraph(State)


def add_age(state: State):
    state["age"] = 20
    return state


def add_name(state: State):
    state["name"] = "John"
    return state


def debug_print(state: State):
    print(state)
    return state


def debug_print_2(state: State):
    print(state)
    return state


graph_builder.add_node("add_age", add_age)
graph_builder.add_node("add_name", add_name)
graph_builder.add_node("debug_print", debug_print)
graph_builder.add_node("debug_print_2", debug_print_2)

graph_builder.add_edge(START, "add_age")
graph_builder.add_edge("add_age", "debug_print")
graph_builder.add_edge("debug_print", "add_name")
graph_builder.add_edge("add_name", "debug_print_2")
graph_builder.add_edge("debug_print_2", END)
graph = graph_builder.compile()
graph.invoke({"messages": [{"role": "user", "content": "Hello, how are you?"}]})
