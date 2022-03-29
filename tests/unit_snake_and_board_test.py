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


def test_snake_init(sample_snake_data):
    snake = Snake(**sample_snake_data)
    assert snake.head == Position(5, 4)
    assert snake.body_and_head == [
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(6, 2),
    ]
    assert snake.neck == Position(5, 3)
    assert snake.tail == Position(6, 2)
    assert len(snake) == 4


def test_next_theoretical_positions(sample_snake):
    assert sample_snake.head == Position(5, 4)
    assert sample_snake.get_next_theoretical_moves() == {
        Position(6, 4): NextStep.RIGHT,
        Position(4, 4): NextStep.LEFT,
        Position(5, 5): NextStep.UP,
        Position(5, 3): NextStep.DOWN,
    }


def test_board_init(sample_board_data):
    my_head = Position(0, 0)
    board = Board(
        my_head=my_head,
        **sample_board_data,
    )
    assert board.height == 11
    assert board.width == 11
    assert board.food == {
        Position(5, 5),
        Position(9, 0),
        Position(2, 6),
    }
    assert len(board.all_snakes) == 2
    snake: Snake = board.all_snakes.get(Position(5, 4))  # type: ignore
    assert len(snake) == 4  # type: ignore
    assert snake.body_and_head[-1] == Position(6, 2)  # type: ignore
    assert snake.tail == Position(6, 2)  # type: ignore
    assert board.my_snake.is_me
    assert snake.is_me == False


def test_get_my_snake(sample_board):
    me = sample_board.my_snake
    assert len(me) == 3
    assert me.neck == Position(1, 0)
    assert me.tail == Position(2, 0)


def test_is_wall(sample_board):
    assert not sample_board.is_wall(Position(0, 0))
    assert not sample_board.is_wall(Position(3, 3))
    assert not sample_board.is_wall(Position(10, 10))
    assert not sample_board.is_wall(Position(0, 10))
    assert not sample_board.is_wall(Position(10, 0))
    assert sample_board.is_wall(Position(-1, 3))
    assert sample_board.is_wall(Position(2, -3))
    assert sample_board.is_wall(Position(11, 3))
    assert sample_board.is_wall(Position(5, 11))
    assert sample_board.is_wall(Position(15, 15))
    assert sample_board.is_wall(Position(-3, 15))
    assert sample_board.is_wall(Position(-3, -8))


@pytest.mark.parametrize(
    "snake_str, next_step, is_food_available, expected_outcome",
    [
        ("snake_in_block", NextStep.LEFT, False, True),  # neck without food
        ("snake_in_block", NextStep.LEFT, True, True),  # neck with food
        ("snake_in_block", NextStep.UP, False, True),  # body without food
        ("snake_in_block", NextStep.UP, True, True),  # body with food
        ("snake_in_block", NextStep.RIGHT, False, False),  # tail without food
        ("snake_in_block", NextStep.RIGHT, True, True),  # tail with food
        ("snake_in_block", NextStep.DOWN, False, False),  # free space without food
        ("snake_in_block", NextStep.DOWN, True, False),  # free space with food
        #
        ("sample_snake", NextStep.UP, False, False),  # free space without food
        ("sample_snake", NextStep.LEFT, False, False),  # free space without food
        ("sample_snake", NextStep.RIGHT, False, False),  # free space without food
        ("sample_snake", NextStep.UP, True, False),  # free space with food
        ("sample_snake", NextStep.DOWN, True, True),  # neck with food
        #
        ("snake_origin", NextStep.UP, False, True),  # neck without food
        ("snake_origin", NextStep.UP, True, True),  # neck with food
        ("snake_origin", NextStep.RIGHT, False, False),  # free space without food
        #
        (
            "snake_middle_short",
            NextStep.RIGHT,
            False,
            True,
        ),
        ("snake_middle_short", NextStep.RIGHT, True, True),  # neck with food
        ("snake_middle_short", NextStep.LEFT, False, False),  # free space without food
        ("snake_middle_short", NextStep.LEFT, True, False),  # free space with food
        #
        (
            "snake_right_middle_short",
            NextStep.LEFT,
            True,
            True,
        ),  # neck space with food
        (
            "snake_right_middle_short",
            NextStep.LEFT,
            False,
            True,
        ),  # neck space without food
        ("snake_right_middle_short", NextStep.UP, True, False),  # free space with food
        (
            "snake_right_middle_short",
            NextStep.DOWN,
            True,
            False,
        ),  # free space with food
        (
            "snake_right_middle_short",
            NextStep.RIGHT,
            True,
            False,
        ),  # free space with food (even is wall, but this is not checked here)
        (
            "snake_right_middle_short",
            NextStep.UP,
            False,
            False,
        ),  # free space with food
    ],
)
def test_snake_will_bite_itself(
    snake_str,
    next_step: NextStep,
    is_food_available: bool,
    expected_outcome: bool,
    request: pytest.FixtureRequest,
):
    snake = request.getfixturevalue(snake_str)
    assert (
        snake.will_bite_itself(
            next_step,
            is_food_available,
        )
        == expected_outcome
    )


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