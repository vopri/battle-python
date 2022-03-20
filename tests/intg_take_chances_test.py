from battle_snake.entities import NextStep
from battle_snake.interactor import MoveDecision


def test_exclude_dangerous_steps_other_snakes(test_request_move_me_3):
    md = MoveDecision(test_request_move_me_3)
    md._select_chances()
    assert set(md.possible_moves.values()) == {NextStep.RIGHT}
