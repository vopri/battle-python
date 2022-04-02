import pytest
from battle_snake.entities import NextStep, Position
from battle_snake.interactor import MoveDecision


@pytest.mark.skip
@pytest.mark.parametrize(
    "next_possible_steps,filtered_steps",
    [
        (
            {
                Position(-1, 0): NextStep.LEFT,
                Position(0, -1): NextStep.DOWN,
                Position(0, 1): NextStep.UP,
                Position(1, 0): NextStep.RIGHT,
            },
            {
                NextStep.UP,
                NextStep.RIGHT,
            },
        ),
        (
            {
                Position(11, 0): NextStep.RIGHT,
                Position(10, -1): NextStep.DOWN,
                Position(10, 1): NextStep.UP,
                Position(9, 0): NextStep.LEFT,
            },
            {
                NextStep.UP,
                NextStep.LEFT,
            },
        ),
        (
            {
                Position(-1, 10): NextStep.LEFT,
                Position(0, 11): NextStep.UP,
                Position(0, 9): NextStep.DOWN,
                Position(1, 10): NextStep.RIGHT,
            },
            {
                NextStep.DOWN,
                NextStep.RIGHT,
            },
        ),
        (
            {
                Position(11, 10): NextStep.RIGHT,
                Position(10, 11): NextStep.UP,
                Position(10, 9): NextStep.DOWN,
                Position(9, 10): NextStep.LEFT,
            },
            {
                NextStep.DOWN,
                NextStep.LEFT,
            },
        ),
        (
            {
                Position(5, 11): NextStep.UP,
                Position(5, 9): NextStep.DOWN,
                Position(4, 10): NextStep.LEFT,
                Position(6, 10): NextStep.RIGHT,
            },
            {
                NextStep.DOWN,
                NextStep.LEFT,
                NextStep.RIGHT,
            },
        ),
        (
            {
                Position(5, -1): NextStep.DOWN,
                Position(5, 1): NextStep.UP,
                Position(4, 0): NextStep.LEFT,
                Position(6, 0): NextStep.RIGHT,
            },
            {
                NextStep.UP,
                NextStep.LEFT,
                NextStep.RIGHT,
            },
        ),
        (
            {
                Position(11, 5): NextStep.RIGHT,
                Position(10, 6): NextStep.UP,
                Position(9, 5): NextStep.LEFT,
                Position(10, 4): NextStep.DOWN,
            },
            {
                NextStep.UP,
                NextStep.LEFT,
                NextStep.DOWN,
            },
        ),
        (
            {
                Position(-1, 5): NextStep.LEFT,
                Position(0, 6): NextStep.UP,
                Position(1, 5): NextStep.RIGHT,
                Position(0, 4): NextStep.DOWN,
            },
            {
                NextStep.UP,
                NextStep.RIGHT,
                NextStep.DOWN,
            },
        ),
        (
            {
                Position(4, 5): NextStep.LEFT,
                Position(6, 5): NextStep.RIGHT,
                Position(5, 6): NextStep.UP,
                Position(5, 4): NextStep.DOWN,
            },
            {
                NextStep.LEFT,
                NextStep.RIGHT,
                NextStep.UP,
                NextStep.DOWN,
            },
        ),
    ],
)
def test_filter_walls(
    sample_move_decision: MoveDecision,
    next_possible_steps,
    filtered_steps,
):
    sample_move_decision.possible_moves = next_possible_steps
    sample_move_decision._avoid_walls()
    assert set(sample_move_decision.possible_moves.values()) == filtered_steps
