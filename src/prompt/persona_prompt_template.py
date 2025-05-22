from dataclasses import dataclass

from interface.character import Character, Persona
from prompt.prompt_template import PromptParam, PromptTemplate


@dataclass
class PersonaPromptParam(PromptParam):
    character: Character
    persona: Persona


class PersonaPromptTemplate(PromptTemplate):
    def __init__(self, template_name: str = "persona.j2"):
        super().__init__(template_name)

    def render(self, params: PersonaPromptParam) -> str:
        return self.template.render(params)
