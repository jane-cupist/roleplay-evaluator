import argparse
from datetime import datetime

import yaml
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from toolz import pipe

from agent.companion_agent import CompanionAgent
from agent.final_evaluator_agent import FinalEvaluatorAgent
from agent.persona_character_agent import PersonaAgent
from agent.turn_evaluator_agent import TurnEvaluatorAgent
from factory.model_factory import ModelFactory
from interface.chat_state import ChatState


def initialize_agents(model_name: str):
    companion_model = ModelFactory.create_model(model_name, temperature=0.7)

    persona_model = ModelFactory.create_model(temperature=0.7)
    evaluator_model = ModelFactory.create_model(temperature=0.7)
    final_evaluator_model = ModelFactory.create_model(temperature=0.7)

    return companion_model, persona_model, evaluator_model, final_evaluator_model


def get_character_indices():
    default_index = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona-index", type=int)
    parser.add_argument("--agent-index", type=int)

    args = parser.parse_args()

    return {
        "persona_index": args.persona_index or default_index,
        "companion_index": args.companion_index or default_index,
    }


def load_character_data(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def router(state: ChatState, turn_limit: int) -> str:
    if len(state["messages"]) // 2 == turn_limit:
        return "final_evaluator"

    return "companion"


def set_model_name(state: ChatState, model_name: str) -> ChatState:
    state["model"] = model_name

    return state


def set_turn_limit(state: ChatState, turn_limit: int) -> ChatState:
    state["turn_limit"] = turn_limit

    return state


def add_nodes_to_graph(
    model_name: str,
    turn_limit: int,
    companion_model,
    persona_model,
    evaluator_model,
    final_evaluator_model,
    persona_data,
    companion_data,
):
    companion_node = CompanionAgent(model=companion_model, character=companion_data)
    persona_node = PersonaAgent(model=persona_model, character=persona_data)
    evaluator_node = TurnEvaluatorAgent(
        model=evaluator_model, criteria=persona_data["evaluation_criterias"]
    )
    final_evaluator_node = FinalEvaluatorAgent(
        model=final_evaluator_model, criteria=persona_data["evaluation_criterias"]
    )

    workflow = StateGraph(ChatState)
    workflow.add_node("companion", companion_node)
    workflow.add_node("persona", persona_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("final_evaluator", final_evaluator_node)
    workflow.add_node(
        "set_model_name", lambda state: set_model_name(state, model_name)
    )  # 모델 이름 설정
    workflow.add_node(
        "set_turn_limit", lambda state: set_turn_limit(state, turn_limit)
    )  # 턴 제한 설정

    return workflow


def add_edges_to_graph(workflow, turn_limit: int):
    workflow.add_edge(START, "persona")
    workflow.add_edge("companion", "persona")
    workflow.add_edge("persona", "evaluator")

    workflow.add_conditional_edges(
        "evaluator",
        lambda state: router(state, turn_limit),
        {"companion": "companion", "final_evaluator": "final_evaluator"},
    )
    workflow.add_edge("final_evaluator", "set_model_name")
    workflow.add_edge("set_model_name", "set_turn_limit")
    workflow.add_edge("set_turn_limit", END)

    return workflow


def start_simulation(workflow, companion_data):
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    config = {
        "configurable": {"thread_id": "abc123"},
        "recursion_limit": 400,  # 재귀 제한을 400으로 증가
        "timeout": 60000,
    }

    query = companion_data["initial_message"]
    app.invoke({"messages": [AIMessage(content=query)]}, config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona-index", type=int)
    parser.add_argument("--companion_index", type=int)
    parser.add_argument("--model", type=str)  # gp, cl, ge, ll
    parser.add_argument("--limit", type=int)  #
    args = parser.parse_args()

    print(f"[model: {args.model}, limit: {args.limit}] START / {datetime.now()}")

    persona_index = args.persona_index or 0
    companion_index = args.companion_index or 0
    turn_limit = args.limit or 1

    character_data = load_character_data("asset/characters.yaml")

    persona_data = character_data["personas"][persona_index]
    companion_data = character_data["companions"][companion_index]

    pipe(
        initialize_agents(args.model),
        lambda models: add_nodes_to_graph(
            args.model, turn_limit, *models, persona_data, companion_data
        ),
        lambda workflow: add_edges_to_graph(workflow, turn_limit),
        lambda workflow: start_simulation(workflow, companion_data),
    )

    print(f"[model: {args.model}, limit: {args.limit}] END / {datetime.now()}")
