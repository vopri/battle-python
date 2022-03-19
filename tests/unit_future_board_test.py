import pytest
from battle_snake.entities import Board, FutureBoard, Position


def test_future_board_init(test_board: Board):
    future_board = FutureBoard(test_board)
    assert test_board.height == future_board.height
    assert test_board.width == future_board.width
    assert future_board.food == {
        # Position(2, 6), # eaten
        # Position(5, 4), # eaten
        Position(5, 5),
        Position(9, 0),
    }
    assert len(test_board.food) == 4
    assert len(future_board.food) == 2
    assert len(test_board.all_snakes) == 7


def test_future_board_all_possible_snakes(test_board: Board):
    future_board = FutureBoard(test_board)
    assert len(future_board.all_possible_snakes) == 13
    expected_heads = {
        Position(x=1, y=6),
        Position(x=2, y=5),
        Position(x=3, y=6),
        Position(x=4, y=2),
        Position(x=4, y=4),
        Position(x=4, y=4),
        Position(x=4, y=6),
        Position(x=4, y=10),
        Position(x=5, y=5),
        Position(x=5, y=5),
        Position(x=5, y=9),
        Position(x=6, y=4),
        Position(x=9, y=10),
    }
    assert {snake.head for snake in future_board.all_possible_snakes} == expected_heads

    # for snake in sorted(future_board.all_possible_snakes, key=lambda snake: snake.head):  # type: ignore
    #     print(snake.head)


@pytest.mark.parametrize(
    "position,is_other_snake_body_there",
    [
        (Position(1, 3), False),  # nothing
        (Position(6, 3), True),
        (Position(5, 5), False),  # two heads
        (Position(5, 4), True),
        (Position(4, 5), True),
        (Position(1, 0), False),  # myself in current board
        (Position(5, 10), True),
    ],
)
def test_future_board_is_other_snake_body(
    test_board: Board, position, is_other_snake_body_there
):
    future_board = FutureBoard(test_board)
    assert (
        future_board.is_other_snake_body_on_this(position) == is_other_snake_body_there
    )


def test_calc_snake_head_risk_value(test_board: Board):
    future_board = FutureBoard(test_board)
    risk_value = future_board.calc_snake_head_risk_value(Position(4, 4))
    assert risk_value >= 0
    assert risk_value <= 1
    assert risk_value == (1 / 3) + (1 / 3)
