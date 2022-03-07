from pdb import post_mortem

import pytest
from battle_snake.entities import Board, NextStep, Position, Snake


def test_postion_init():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos.x == 3
    assert pos.y == 2


def test_postion_equal():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos == Position(3, 2)


def test_snake_init(snake_data):
    snake = Snake(**snake_data)
    assert snake.head == Position(5, 4)
    assert snake.body_incl_head == [
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(6, 2),
    ]
    assert snake.neck == Position(5, 3)
    assert snake.tail == Position(6, 2)
    assert len(snake) == 4


def test_next_theoretical_positions(snake):
    assert snake.head == Position(5, 4)
    assert snake.next_theoretical_head_positions_and_moves() == {
        Position(6, 4): NextStep.RIGHT,
        Position(4, 4): NextStep.LEFT,
        Position(5, 5): NextStep.UP,
        Position(5, 3): NextStep.DOWN,
    }


@pytest.fixture
def snake(snake_data) -> Snake:
    return Snake(**snake_data)


@pytest.fixture
def snake_data() -> dict:
    return {
        "id": "snake-b67f4906-94ae-11ea-bb37",
        "name": "Another Snake",
        "health": 16,
        "body": [
            {"x": 5, "y": 4},
            {"x": 5, "y": 3},
            {"x": 6, "y": 3},
            {"x": 6, "y": 2},
        ],
        "latency": "222",
        "head": {"x": 5, "y": 4},
        "length": 4,
        "shout": "I'm not really sure...",
        "squad": "",
        "customizations": {"color": "#26CF04", "head": "silly", "tail": "curled"},
    }


def test_board_init(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    assert board.height == 11
    assert board.width == 11
    assert board.food == {
        Position(5, 5),
        Position(9, 0),
        Position(2, 6),
    }
    assert len(board.all_snakes) == 2
    snake_on_5_4 = board.all_snakes.get(Position(5, 4))
    assert len(snake_on_5_4) == 4  # type: ignore
    assert snake_on_5_4.body_incl_head[-1] == Position(6, 2)  # type: ignore


def test_get_my_snake(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    me = board.my_snake
    assert len(me) == 3
    assert me.neck == Position(1, 0)


def test_is_wall(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    assert not board.is_wall(Position(0, 0))
    assert not board.is_wall(Position(3, 3))
    assert not board.is_wall(Position(10, 10))
    assert not board.is_wall(Position(0, 10))
    assert not board.is_wall(Position(10, 0))
    assert board.is_wall(Position(-1, 3))
    assert board.is_wall(Position(2, -3))
    assert board.is_wall(Position(11, 3))
    assert board.is_wall(Position(5, 11))
    assert board.is_wall(Position(15, 15))
    assert board.is_wall(Position(-3, 15))
    assert board.is_wall(Position(-3, -8))


@pytest.fixture
def board_data() -> dict:
    return {
        "height": 11,
        "width": 11,
        "food": [{"x": 5, "y": 5}, {"x": 9, "y": 0}, {"x": 2, "y": 6}],
        "hazards": [{"x": 3, "y": 2}],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 54,
                "body": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}],
                "latency": "111",
                "head": {"x": 0, "y": 0},
                "length": 3,
                "shout": "why are we shouting??",
                "squad": "",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel",
                },
            },
            {
                "id": "snake-b67f4906-94ae-11ea-bb37",
                "name": "Another Snake",
                "health": 16,
                "body": [
                    {"x": 5, "y": 4},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                    {"x": 6, "y": 2},
                ],
                "latency": "222",
                "head": {"x": 5, "y": 4},
                "length": 4,
                "shout": "I'm not really sure...",
                "squad": "",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled",
                },
            },
        ],
    }


@pytest.fixture
def board_data_two() -> dict:
    return {
        "height": 11,
        "width": 11,
        "food": [{"x": 5, "y": 5}, {"x": 9, "y": 0}, {"x": 2, "y": 6}],
        "hazards": [{"x": 3, "y": 2}],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 54,
                "body": [
                    {"x": 0, "y": 1},
                    {"x": 0, "y": 0},
                    {"x": 1, "y": 0},
                    {"x": 2, "y": 0},
                ],
                "latency": "111",
                "head": {"x": 0, "y": 1},
                "length": 4,
                "shout": "why are we shouting??",
                "squad": "",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel",
                },
            },
            {
                "id": "snake-b67f4906-94ae-11ea-bb37",
                "name": "Another Snake",
                "health": 16,
                "body": [
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 4},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                ],
                "latency": "222",
                "head": {"x": 5, "y": 5},
                "length": 4,
                "shout": "I'm not really sure...",
                "squad": "",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled",
                },
            },
        ],
    }