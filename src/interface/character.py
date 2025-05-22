from typing import List, Protocol

from interface.evaluation_criteria import EvaluationCriteria


class Character(Protocol):
    name: str
    character_archetype: str
    description: str
    story_background: str


class Persona(Protocol):
    name: str
    character_archetype: str
    description: str
    story_background: str


class Character(Character):
    initial_message: str


class PersonaCharacter(Character):
    evaluation_criterias: List[EvaluationCriteria]
