from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class PromptParam(ABC):
    pass


class PromptTemplate(ABC):
    def __init__(self, template_name: str):
        template_dir = Path("asset/template/prompt")
        self.env = Environment(
            loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
        )
        self.template = self.env.get_template(template_name)

    @abstractmethod
    def render(self, params: PromptParam) -> str:
        pass
