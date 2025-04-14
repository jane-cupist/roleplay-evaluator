from langchain_core.language_models import BaseChatModel


class Agent:
    def __init__(self, model: BaseChatModel):
        self.model = model
