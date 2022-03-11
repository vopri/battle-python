from battle_snake.entities import NextStep, Snake


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
