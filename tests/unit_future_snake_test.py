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
    print(snake)
    assert str(snake) == snake_as_str


def test_snake_body_withoud_head(snake_origin):
    assert snake_origin.body_without_head == [Position(0, 1), Position(0, 2)]


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_right_without_food.body_incl_head
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_left_without_food.body_incl_head
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, food=False
    )
    assert (
        future_snake.body_incl_head == snake_long_future_up_without_food.body_incl_head
    )


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_2_future_down_without_food.body_incl_head
    )
