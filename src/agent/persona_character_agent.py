from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from interface.agent import Agent
from interface.character import PersonaCharacter
from interface.chat_state import ChatState
from prompt.prompt_template import PromptTemplate
from utils.retry_utils import retry_with_exponential_backoff


class PersonaAgent(Agent):
    def __init__(self, model: BaseChatModel, character: PersonaCharacter):
        super().__init__(model)
        self.character = character

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        last_message = messages[-1]

        prompt = PersonaAgent.make_prompt(self.character)
        chain = prompt | self.model

        response = chain.invoke(
            {"messages": messages[:-1], "input": last_message},
            {"timeout": 60000},
        )

        state["messages"] = messages + [HumanMessage(content=response.content)]
        return state

    @staticmethod
    def make_prompt(character: PersonaCharacter) -> ChatPromptTemplate:
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
