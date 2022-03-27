import pytest
from battle_snake.entities import NextStep, Position, Snake


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, is_food_available=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_right_without_food.body_incl_head
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, is_food_available=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_left_without_food.body_incl_head
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, is_food_available=False
    )
    assert (
        future_snake.body_incl_head == snake_long_future_up_without_food.body_incl_head
    )


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_2_future_down_without_food.body_incl_head
    )


def test_future_snake_mini_without_food_growing():
    baby_snake = Snake(**{"body": [{"x": 7, "y": 4}]})
    future_snake = baby_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert len(future_snake) == len(baby_snake) + 1
    assert (
        future_snake.body_incl_head
        == Snake(**{"body": [{"x": 7, "y": 3}, {"x": 7, "y": 4}]}).body_incl_head
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_incl_head
        == Snake(
            **{"body": [{"x": 7, "y": 2}, {"x": 7, "y": 3}, {"x": 7, "y": 4}]}
        ).body_incl_head
    )
    future_snake = future_snake.calculate_future_snake(
        next_step=NextStep.DOWN, is_food_available=False
    )
    assert (
        future_snake.body_incl_head
        == Snake(
            **{"body": [{"x": 7, "y": 1}, {"x": 7, "y": 2}, {"x": 7, "y": 3}]}
        ).body_incl_head
    )
