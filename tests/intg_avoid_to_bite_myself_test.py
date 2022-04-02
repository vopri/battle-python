import pytest
from battle_snake.entities import NextStep, Snake
from battle_snake.interactor import MoveDecision


@pytest.mark.skip
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
        (
            "snake_in_block",
            False,
            {NextStep.RIGHT, NextStep.DOWN},
        ),
        (
            "snake_in_block",
            True,
            {NextStep.DOWN},
        ),
    ],
)
def test_avoid_my_bite_myself(
    sample_move_decision: MoveDecision,
    snake_fix_str: str,
    food: bool,
    expected_steps: set[NextStep],
    request: pytest.FixtureRequest,
):
    _arrange_test_avoid_bite_myself(sample_move_decision, snake_fix_str, food, request)
    sample_move_decision._avoid_myself()
    assert set(sample_move_decision.possible_moves.values()) == expected_steps


def _arrange_test_avoid_bite_myself(sample_move_decision, snake_fix_str, food, request):
    snake: Snake = request.getfixturevalue(snake_fix_str)
    sample_move_decision.board.all_snakes = {snake.head: snake}
    sample_move_decision.board._my_head = snake.head
    sample_move_decision.possible_moves = (
        sample_move_decision.me.get_next_theoretical_moves()
    )
    if food:
        sample_move_decision.board.food = {snake.head}
    else:
        sample_move_decision.board.food = set()
