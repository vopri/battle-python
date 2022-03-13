from battle_snake.entities import NextStep
from battle_snake.interactor import MoveDecision


def test_decide_sample_request(sample_move_decision: MoveDecision):
    assert sample_move_decision.decide() == NextStep.UP
