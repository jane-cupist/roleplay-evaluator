from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from interface.agent import Agent
from interface.character import CompanionCharacter
from interface.chat_state import ChatState
from prompt.prompt_template import PromptTemplate
from utils.retry_utils import retry_with_exponential_backoff


class CompanionAgent(Agent):
    def __init__(self, model: BaseChatModel, character: CompanionCharacter):
        super().__init__(model)
        self.character = character

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        last_message = messages[-1].content if messages else ""

        response = (CompanionAgent.make_prompt(self.character) | self.model).invoke(
            {"messages": messages, "input": last_message},
            {"timeout": 60000},
        )

        state["messages"] = messages + [AIMessage(content=response.content)]
        return state

    @staticmethod
    def make_prompt(character: CompanionCharacter) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    PromptTemplate().render_character_prompt(character),
                ),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}"),
            ]
        )
