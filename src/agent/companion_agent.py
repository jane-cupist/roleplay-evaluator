from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from interface.agent import Agent
from interface.character import Character, Persona
from interface.chat_state import ChatState
from prompt.character_prompt_template import (
    CharacterPromptParam,
    CharacterPromptTemplate,
)
from utils.logger import chat_logger
from utils.retry_utils import retry_with_exponential_backoff


class CompanionAgent(Agent):
    def __init__(self, model: BaseChatModel, character: Character, persona: Persona):
        super().__init__(model)
        self.character = character
        self.persona = persona

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        last_message = messages[-1]

        prompt = self.make_prompt()
        chain = prompt | self.model

        message_contents = [f"{msg.content}" for msg in messages[:-1]]

        response = chain.invoke(
            input={"messages": message_contents, "input": last_message.content},
            config={"timeout": 60000},
        )

        chat_logger.info(f"[Turn {len(messages) // 2 + 1}]")
        chat_logger.info(f"companion: {response.content}")

        return {"messages": [AIMessage(content=response.content)]}

    def make_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    CharacterPromptTemplate().render(
                        CharacterPromptParam(
                            character=self.character, persona=self.persona
                        ).__dict__
                    ),
                ),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}"),
                ("ai", self.make_force_comply_message()),
            ]
        )

    def make_force_comply_message(self) -> str:
        return f"""
Understood, I will simulate what happened next around {self.persona['name']}, within the <lore> and following all <rules>. In particular, I remember that writing {self.persona['name']}'s words or actions is off-limits; I'll stop immediately when it's {self.persona['name']}'s turn to act.
To maintain variety, my plan is to write up to 140 words this time.
My response:"""
