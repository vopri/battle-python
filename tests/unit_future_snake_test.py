import pytest
from battle_snake.entities import NextStep, Position, Snake


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
