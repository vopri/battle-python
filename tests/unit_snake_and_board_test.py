from turtle import down

import pytest
from battle_snake.entities import (
    Board,
    GameBoardBounderies,
    NextStep,
    Position,
    PossibleFutureBoard,
    Snake,
)


def test_postion_init():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos.x == 3
    assert pos.y == 2


def test_postion_equal():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos == Position(3, 2)


def test_snake_init(sample_snake_data):
    snake = Snake.from_dict(**sample_snake_data)
    assert snake.head == Position(5, 4)
    assert snake.head_and_body == [
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(6, 2),
    ]
    assert len(snake) == 4
    assert snake.id == Position(5, 4)


def test_snake_bites_itself():
    snake = Snake(
        [
            Position(4, 4),
            Position(4, 5),
            Position(3, 5),
            Position(3, 4),
            Position(4, 4),
            Position(4, 3),
        ]
    )
    assert snake.bites_itself()


def test_snake_bites_not_itself():
    snake = Snake(
        [
            Position(5, 5),
            Position(4, 5),
            Position(3, 5),
            Position(3, 4),
            Position(4, 4),
            Position(4, 3),
        ]
    )
    assert not snake.bites_itself()


def test_board_init(sample_request):
    board = Board.from_dict(sample_request)
    assert board.bounderies == GameBoardBounderies(11, 11)
    assert board.food == {
        Position(5, 5),
        Position(9, 0),
        Position(2, 6),
    }
    assert len(board.snakes) == 2
    snake: Snake = [
        snake for snake in board.snakes if snake.head == Position(5, 4)
    ].pop()
    assert len(snake) == 4
    assert snake.head_and_body[-1] == Position(6, 2)
    assert board.my_snake.is_me
    assert snake.is_me == False


def test_get_my_snake(sample_board):
    me = sample_board.my_snake
    assert len(me) == 3


def test_is_wall(sample_board: Board):
    future_board = PossibleFutureBoard(sample_board)
    assert not future_board.is_wall(Position(0, 0))
    assert not future_board.is_wall(Position(3, 3))
    assert not future_board.is_wall(Position(10, 10))
    assert not future_board.is_wall(Position(0, 10))
    assert not future_board.is_wall(Position(10, 0))
    assert future_board.is_wall(Position(-1, 3))
    assert future_board.is_wall(Position(2, -3))
    assert future_board.is_wall(Position(11, 3))
    assert future_board.is_wall(Position(5, 11))
    assert future_board.is_wall(Position(15, 15))
    assert future_board.is_wall(Position(-3, 15))
    assert future_board.is_wall(Position(-3, -8))


@pytest.mark.parametrize(
    "snake_name, snake_as_str",
    [
        (
            "snake_origin",
            "|===========|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|x··········|\n|x··········|\n|o··········|\n|===========|",
        ),
        (
            "sample_snake",
            "|===========|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|···········|\n|·····o·····|\n|·····xx····|\n|······x····|\n|···········|\n|···········|\n|===========|",
        ),
    ],
)
def test_print_snake(
    snake_name: str, snake_as_str: str, request: pytest.FixtureRequest
):
    snake: Snake = request.getfixturevalue(snake_name)
    assert str(snake) == snake_as_str


def test_snake_body_withoud_head(snake_origin):
    assert snake_origin.body_without_head == [Position(0, 1), Position(0, 2)]


def test_find_nearest_food(sample_board: Board):
    nearest_food = sample_board.get_food_ordered_by_distance(Position(5, 7))
    assert len(nearest_food) == 3
    nf0 = nearest_food[0]
    assert nf0[0] == {NextStep.DOWN}
    assert nf0[1] == 2
    assert nf0[2] == Position(5, 5)

    nf1 = nearest_food[1]
    assert nf1[0] == {NextStep.DOWN, NextStep.LEFT}
    assert nf1[1] == 4
    assert nf1[2] == Position(2, 6)

    nf2 = nearest_food[2]
    assert nf2[0] == {NextStep.DOWN, NextStep.RIGHT}
    assert nf2[1] == 11
    assert nf2[2] == Position(9, 0)


def test_board_move_snake(solo_board_2: Board):
    assert solo_board_2.move_snake(solo_board_2.my_snake, NextStep.UP) == Position(5, 9)
    assert solo_board_2.move_snake(solo_board_2.my_snake, NextStep.DOWN) == Position(
        5, 7
    )
    assert solo_board_2.move_snake(solo_board_2.my_snake, NextStep.LEFT) == Position(
        4, 8
    )
    assert solo_board_2.move_snake(solo_board_2.my_snake, NextStep.RIGHT) == Position(
        6, 8
    )
