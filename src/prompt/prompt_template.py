from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from interface.character import Character
from interface.evaluation_criteria import EvaluationCriteria


class PromptTemplate:
    def __init__(self):
        template_dir = Path("asset/template/prompt")
        self.env = Environment(
            loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
        )

    def render_character_prompt(self, character: Character) -> str:
        template = self.env.get_template("character.j2")
        return template.render(
            character=character,
        )

    def render_evaluator_prompt(
        self, messages: list, criteria: EvaluationCriteria
    ) -> str:
        template = self.env.get_template("evaluator.j2")
        return template.render(messages=messages, criteria=criteria)
