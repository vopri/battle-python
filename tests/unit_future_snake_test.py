import pytest
from battle_snake.entities import (
    Board,
    FutureSnake,
    GameBoardBounderies,
    NextStep,
    Position,
    Snake,
)


def test_future_snake_init(sample_snake: Snake):
    next_step = NextStep.UP
    is_food_available = True
    future_snake = FutureSnake(sample_snake, next_step, is_food_available)
    assert future_snake.step_made_to_get_here == next_step
    assert future_snake._is_food_available_at_creation_time == is_food_available
    assert future_snake.mother == sample_snake
    assert future_snake.head == Position(5, 5)
    assert future_snake.get_my_first_step() == NextStep.UP
    assert sample_snake.head == Position(5, 4)
    assert sample_snake.id == future_snake.id
    assert (
        future_snake.calculate_future_snake(NextStep.DOWN).my_first_step == NextStep.UP
    )


def test_sample_board_future_snake_is_me_marker(sample_board: Board):
    my_future_snake: FutureSnake = sample_board.my_snake.calculate_future_snake(
        NextStep.UP, True
    )
    assert my_future_snake.is_me
    other_snake: Snake = [
        snake for snake in sample_board.snakes if snake.head == Position(5, 4)
    ].pop()
    other_future_snake = other_snake.calculate_future_snake(NextStep.DOWN)
    assert other_future_snake.is_me == False


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, is_food_available=False
    )
    assert (
        future_snake.head_and_body == snake_long_future_right_without_food.head_and_body
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, is_food_available=False
    )
    assert (
        future_snake.head_and_body == snake_long_future_left_without_food.head_and_body
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, is_food_available=False
    )
    assert future_snake.head_and_body == snake_long_future_up_without_food.head_and_body


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.head_and_body
        == snake_long_2_future_down_without_food.head_and_body
    )


def test_future_snake_mini_without_food_growing():
    baby_snake = Snake.from_dict(**{"body": [{"x": 7, "y": 4}]})
    future_snake = baby_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert len(future_snake) == len(baby_snake) + 1
    assert (
        future_snake.head_and_body
        == Snake.from_dict(
            **{"body": [{"x": 7, "y": 3}, {"x": 7, "y": 4}]}
        ).head_and_body
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.head_and_body
        == Snake.from_dict(
            **{"body": [{"x": 7, "y": 2}, {"x": 7, "y": 3}, {"x": 7, "y": 4}]}
        ).head_and_body
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.head_and_body
        == Snake.from_dict(
            **{"body": [{"x": 7, "y": 1}, {"x": 7, "y": 2}, {"x": 7, "y": 3}]}
        ).head_and_body
    )


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


def test_future_snake_of_future_snake():
    snake = Snake([Position(5, 5)], is_me=True)
    future_snake = snake.calculate_future_snake(NextStep.DOWN)
    future_snake = future_snake.calculate_future_snake(NextStep.DOWN)
    future_snake = future_snake.calculate_future_snake(NextStep.RIGHT)
    future_snake = future_snake.calculate_future_snake(NextStep.UP)
    future_snake = future_snake.calculate_future_snake(
        NextStep.LEFT, is_food_available=True
    )
    assert future_snake.head == Position(5, 4)
    assert len(future_snake) == 4
    assert future_snake.get_my_first_step() == NextStep.DOWN
