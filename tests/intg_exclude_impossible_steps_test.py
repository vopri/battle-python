import pytest
from battle_snake.entities import Board, NextStep, Snake
from battle_snake.interactor import MoveDecision


@pytest.mark.parametrize(
    "snake_fix_str, expected_steps",
    [
        (
            "snake_origin",
            {NextStep.RIGHT},
        ),
        (
            "snake_in_block",
            {NextStep.RIGHT, NextStep.DOWN},
        ),
        (
            "snake_top_middle_short",
            {NextStep.LEFT, NextStep.DOWN},
        ),
        (
            "snake_bottom_middle_short",
            {NextStep.LEFT, NextStep.UP},
        ),
        (
            "snake_left_middle_short",
            {NextStep.DOWN, NextStep.UP},
        ),
        (
            "snake_right_middle_short",
            {NextStep.DOWN, NextStep.UP},
        ),
        (
            "snake_top_right_short",
            {NextStep.LEFT},
        ),
        (
            "snake_top_right_short_collision_same_size",
            {NextStep.DOWN},
        ),
        (
            "snake_long",
            {NextStep.UP, NextStep.LEFT, NextStep.RIGHT},
        ),
        (
            "snake_long_2",
            {NextStep.UP, NextStep.LEFT, NextStep.DOWN},
        ),
        (
            "snake_long_2_future_down_without_food",
            {NextStep.LEFT, NextStep.DOWN},
        ),
    ],
)
def test_exclude_impossible_steps(
    sample_move_decision: MoveDecision,
    snake_fix_str: str,
    expected_steps: set[NextStep],
    request: pytest.FixtureRequest,
):
    _arrange_test_exclude_impossible_steps(sample_move_decision, snake_fix_str, request)
    sample_move_decision._exclude_impossible_moves()
    assert set(sample_move_decision.possible_moves.values()) == expected_steps


def _arrange_test_exclude_impossible_steps(
    sample_move_decision, snake_fix_str, request
):
    snake: Snake = request.getfixturevalue(snake_fix_str)
    sample_move_decision.board.all_snakes = {snake.head: snake}
    sample_move_decision.board._my_head = snake.head
    sample_move_decision.possible_moves = (
        sample_move_decision.me.get_next_theoretical_moves()
    )


def test_exclude_impossible_steps_other_snakes(test_request_move_me_1):
    md = MoveDecision(test_request_move_me_1)
    md._exclude_impossible_moves()
    assert set(md.possible_moves.values()) == {NextStep.RIGHT}


def test_exclude_dangerous_steps_other_snakes(test_request_move_me_2):
    md = MoveDecision(test_request_move_me_2)
    md._exclude_dangerous_moves()
    assert set(md.possible_moves.values()) == {NextStep.RIGHT, NextStep.UP}
