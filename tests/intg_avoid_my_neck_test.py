import pytest
from battle_snake.entities import NextStep, Snake
from battle_snake.interactor import MoveDecision


@pytest.mark.parametrize(
    "snake_fix_str, food, expected_steps",
    [
        (
            "snake_right_middle_short",
            False,
            {NextStep.UP, NextStep.DOWN, NextStep.RIGHT},
        ),
        (
            "snake_middle_short",
            False,
            {NextStep.UP, NextStep.DOWN, NextStep.LEFT},
        ),
        (
            "snake_origin",
            False,
            {NextStep.RIGHT, NextStep.DOWN, NextStep.LEFT},
        ),
        (
            "snake_top_right_short",
            False,
            {NextStep.RIGHT, NextStep.UP, NextStep.LEFT},
        ),
    ],
)
def test_avoid_my_neck(
    sample_move_decision: MoveDecision,
    snake_fix_str: str,
    food: bool,
    expected_steps: set[NextStep],
    request: pytest.FixtureRequest,
):
    _arrange_test_avoid_my_neck(sample_move_decision, snake_fix_str, food, request)
    sample_move_decision._avoid_my_neck()
    assert set(sample_move_decision.possible_moves.values()) == expected_steps


def _arrange_test_avoid_my_neck(sample_move_decision, snake_fix_str, food, request):
    snake: Snake = request.getfixturevalue(snake_fix_str)
    sample_move_decision.board.all_snakes = {snake.head: snake}
    sample_move_decision.board.my_head = snake.head
    sample_move_decision.possible_moves = (
        sample_move_decision.me.next_theoretical_head_positions_and_moves()
    )
    if food:
        sample_move_decision.board.food = {snake.head}
    else:
        sample_move_decision.board.food = set()
