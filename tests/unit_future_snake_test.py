import pytest
from battle_snake.entities import Board, FutureSnake, NextStep, Position, Snake


def test_future_snake_init(sample_snake: Snake):
    next_step = NextStep.UP
    is_food_available = True
    future_snake = FutureSnake(sample_snake, next_step, is_food_available)
    assert future_snake.next_step == next_step
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
