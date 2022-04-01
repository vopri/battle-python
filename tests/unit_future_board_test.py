import pytest
from battle_snake.entities import Board, FutureBoard, Position


def test_future_board_init(test_board: Board):
    future_board = FutureBoard(test_board)
    assert test_board._bounderies == future_board._bounderies
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
    assert len(future_board.all_possible_snakes) == 14
    expected_heads = {
        Position(x=0, y=1),
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


@pytest.mark.parametrize(
    "position,risk_value_as_str",
    [
        (Position(4, 4), "(1 / 3) + (1 / 3)"),
        (Position(6, 4), "1 / 3"),
        (Position(8, 6), "0"),
        (Position(9, 10), "1"),
        (Position(5, 9), "1/2"),
        (Position(0, 1), "0"),  # my own head is no risk at all
    ],
)
def test_calc_snake_head_risk_value(test_board: Board, position, risk_value_as_str):
    future_board = FutureBoard(test_board)
    risk_value = future_board.calc_snake_head_risk_value(position)
    assert risk_value >= 0
    assert risk_value <= 1
    assert risk_value == eval(risk_value_as_str)


@pytest.mark.parametrize(
    "board_name, amount_of_my_survived_snakes",
    [
        ("test_board", 1),
        ("sample_board_move_me_1", 1),
        ("sample_board_move_me_2", 3),
    ],
)
def test_get_my_survived_snakes(
    board_name: str, amount_of_my_survived_snakes: int, request: pytest.FixtureRequest
):
    board = request.getfixturevalue(board_name)
    future_board = FutureBoard(board)
    snakes = future_board.get_my_survived_snakes()
    assert len(snakes) == amount_of_my_survived_snakes
