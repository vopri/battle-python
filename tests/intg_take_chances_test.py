import pytest
from battle_snake.entities import NextStep
from battle_snake.interactor import MoveDecision


@pytest.mark.skip
def test_exclude_dangerous_steps_other_snakes(test_request_move_me_3):
    md = MoveDecision(test_request_move_me_3)
    md._select_best_possible_moves()
    assert set(md.possible_moves.values()) == {NextStep.RIGHT}
