import csv
import os

from langchain_core.language_models import BaseChatModel

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from utils.csv_writer import parse_description_block, save_evaluation_to_csv
from utils.logger import evaluator_logger


class FinalEvaluatorAgent(EvaluatorAgent):
    def __init__(
        self,
        model: BaseChatModel,
        criteria: EvaluationCriteria,
        persona_name: str,
        character_name: str,
        turn_limit: int,
        companion_model: BaseChatModel,
        repeat_count: int,
    ):
        super().__init__(model, criteria, persona_name, character_name)
        self.output_dir = "output"
        self.model_name = companion_model.__class__.__name__
        self.turn_limit = turn_limit
        self.repeat_count = repeat_count

        os.makedirs(self.output_dir, exist_ok=True)

    def _write_final_evaluation_rows(self, writer: csv.writer, result: dict) -> None:
        # 각 기준별 점수와 설명 작성
        for criteria, score in result["criteria_scores"].items():
            writer.writerow(
                [
                    criteria,
                    score,
                    parse_description_block(result["description"]).get(criteria, ""),
                ]
            )

        # 최종 점수 작성
        writer.writerow(["Final Score", result["score"], ""])

    def __call__(self, state: ChatState) -> ChatState:
        evaluation = super().__call__(state["messages"])
        criteria_scores = evaluation["score"]
        criteria_score_description = evaluation["description"]

        result = {
            "criteria_scores": criteria_scores,
            "score": super().calculate_score(criteria_scores),
            "description": criteria_score_description,
        }

        evaluator_logger.info(f"final_score: {result}")

        # CSV 파일로 결과 저장
        save_evaluation_to_csv(
            result=result,
            output_dir=self.output_dir,
            filename_prefix=f"final_{self.model_name}_turn{self.turn_limit}_{self.character_name}_repeat{self.repeat_count}_evaluation_result",
            headers=["Criteria", "Score", "Description"],
            row_writer=self._write_final_evaluation_rows,
        )

        return state
