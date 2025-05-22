from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from interface.agent import Agent
from interface.character import Character, Persona
from interface.chat_state import ChatState
from prompt.persona_prompt_template import (
    PersonaPromptParam,
    PersonaPromptTemplate,
)
from utils.logger import chat_logger
from utils.retry_utils import retry_with_exponential_backoff


class PersonaAgent(Agent):
    def __init__(self, model: BaseChatModel, character: Character, persona: Persona):
        super().__init__(model)
        self.character = character
        self.persona = persona

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        last_message = messages[-1]

        prompt = PersonaAgent.make_prompt(self.character, self.persona)
        chain = prompt | self.model

        message_contents = [f"{msg.content}" for msg in messages[:-1]]

        response = chain.invoke(
            input={"messages": message_contents, "input": last_message.content},
            config={"timeout": 60000},
        )

        chat_logger.info(f"persona: {response.content}")

        return {"messages": [HumanMessage(content=response.content)]}

    @staticmethod
    def make_prompt(character: Character, persona: Persona) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    PersonaPromptTemplate().render(
                        PersonaPromptParam(
                            character=character, persona=persona
                        ).__dict__
                    ),
                ),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}"),
            ]
        )
