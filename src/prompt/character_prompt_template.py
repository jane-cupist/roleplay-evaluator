from dataclasses import dataclass

from interface.character import Character, Persona
from prompt.prompt_template import PromptParam, PromptTemplate


@dataclass
class CharacterPromptParam(PromptParam):
    character: Character
    persona: Persona


class CharacterPromptTemplate(PromptTemplate):
    def __init__(self, template_name: str = "character.j2"):
        super().__init__(template_name)

    def render(self, params: CharacterPromptParam) -> str:
        return self.template.render(params)
