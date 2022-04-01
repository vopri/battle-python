import pytest
from battle_snake.entities import Board, FutureSnake, NextStep, Position, Snake


def test_future_snake_init(sample_snake: Snake):
    next_step = NextStep.UP
    is_food_available = True
    future_snake = FutureSnake(sample_snake, next_step, is_food_available)
    assert future_snake.step_made_to_get_here == next_step
    assert future_snake.is_food_available == is_food_available
    assert future_snake.mother == sample_snake
    assert future_snake.head == Position(5, 5)
    assert sample_snake.head == Position(5, 4)


def test_sample_board_future_snake_is_me_marker(sample_board: Board):
    my_future_snake: FutureSnake = sample_board.my_snake.calculate_future_snake(
        NextStep.UP, True
    )
    assert my_future_snake.is_me
    other_snake: Snake = sample_board.all_snakes.get(Position(5, 4))  # type: ignore
    other_future_snake = other_snake.calculate_future_snake(NextStep.DOWN)
    assert other_future_snake.is_me == False


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, is_food_available=False
    )
    assert (
        future_snake.body_and_head == snake_long_future_right_without_food.body_and_head
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, is_food_available=False
    )
    assert (
        future_snake.body_and_head == snake_long_future_left_without_food.body_and_head
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, is_food_available=False
    )
    assert future_snake.body_and_head == snake_long_future_up_without_food.body_and_head


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_and_head
        == snake_long_2_future_down_without_food.body_and_head
    )


def test_future_snake_mini_without_food_growing():
    baby_snake = Snake(**{"body": [{"x": 7, "y": 4}]})
    future_snake = baby_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert len(future_snake) == len(baby_snake) + 1
    assert (
        future_snake.body_and_head
        == Snake(**{"body": [{"x": 7, "y": 3}, {"x": 7, "y": 4}]}).body_and_head
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_and_head
        == Snake(
            **{"body": [{"x": 7, "y": 2}, {"x": 7, "y": 3}, {"x": 7, "y": 4}]}
        ).body_and_head
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_and_head
        == Snake(
            **{"body": [{"x": 7, "y": 1}, {"x": 7, "y": 2}, {"x": 7, "y": 3}]}
        ).body_and_head
    )


def test_future_snake_bites_itself(snake_in_block: Snake):
    future_snake_down = snake_in_block.calculate_future_snake(NextStep.DOWN)
    assert not future_snake_down.does_bite_itself()
    future_snake_up = snake_in_block.calculate_future_snake(NextStep.UP)
    assert future_snake_up.does_bite_itself()


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
def test_future_snake_will_bite_itself(
    snake_str,
    next_step: NextStep,
    is_food_available: bool,
    expected_outcome: bool,
    request: pytest.FixtureRequest,
):
    snake: Snake = request.getfixturevalue(snake_str)
    future_snake = snake.calculate_future_snake(next_step, is_food_available)
    assert future_snake.does_bite_itself() == expected_outcome


@pytest.mark.parametrize(
    "snake_name, next_step",
    [
        ("sample_snake", NextStep.UP),
        ("sample_snake", NextStep.DOWN),
        ("sample_snake", NextStep.LEFT),
        ("sample_snake", NextStep.RIGHT),
    ],
)
def test_get_my_first_next_step(
    snake_name: str, next_step: NextStep, request: pytest.FixtureRequest
):
    snake = request.getfixturevalue(snake_name)
    future_snake = snake.calculate_future_snake(next_step)
    assert future_snake.get_my_first_step() == next_step
