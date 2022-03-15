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
    assert snake.body_incl_head == [
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
    assert sample_snake.next_theoretical_head_positions_and_moves() == {
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
    snake = board.all_snakes.get(Position(5, 4))
    assert len(snake) == 4  # type: ignore
    assert snake.body_incl_head[-1] == Position(6, 2)  # type: ignore
    assert snake.tail == Position(6, 2)  # type: ignore


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
    "my_snake, other_snake, is_dangerous",
    [
        ("snake_bottom_middle_short", "snake_top_right_short", False),  # far away
        ("snake_long", "snake_middle_short", False),  # head to head (long one wins)
        ("snake_middle_short", "snake_long", True),  # head to head (changed order)
        ("snake_middle_short", "snake_long_2", True),  # head to body
        (
            "snake_top_right_short",
            "snake_top_right_short_collision_same_size",
            True,
        ),  # head to head same size
        (
            "snake_top_right_short_collision_same_size",
            "snake_top_right_short",
            True,
        ),  # head to head same size (changed order)
    ],
)
def test_is_dangerous(
    my_snake, other_snake, is_dangerous, request: pytest.FixtureRequest
):
    my_snake = request.getfixturevalue(my_snake)
    other_snake = request.getfixturevalue(other_snake)
    assert my_snake.is_dangerous(other_snake) == is_dangerous


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
        # TODO: unclear rule for special case: very short snake with head and tail only: will it bite into his neck (without food)? Have to test with real engine
        # (
        #     "snake_middle_short",
        #     NextStep.RIGHT,
        #     False,
        #     True,
        # ),  # ERROR  # neck without food
        ("snake_middle_short", NextStep.RIGHT, True, True),  # neck with food
        ("snake_middle_short", NextStep.LEFT, False, False),  # free space without food
        ("snake_middle_short", NextStep.LEFT, True, False),  # free space with food
        #
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
