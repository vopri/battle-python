from battle_snake.entities import Snake
from pytest import fixture


@fixture
def sample_snake_data() -> dict:
    return {
        "body": [
            {"x": 5, "y": 4},
            {"x": 5, "y": 3},
            {"x": 6, "y": 3},
            {"x": 6, "y": 2},
        ],
    }


@fixture
def sample_snake(sample_snake_data) -> Snake:
    return Snake(**sample_snake_data)


@fixture
def snake_in_block():
    return Snake(
        **{
            "body": [
                {"x": 7, "y": 4},
                {"x": 6, "y": 4},
                {"x": 6, "y": 5},
                {"x": 7, "y": 5},
                {"x": 8, "y": 5},
                {"x": 8, "y": 4},
            ],
        }
    )


@fixture
def snake_origin():
    return Snake(
        **{
            "body": [
                {"x": 0, "y": 0},
                {"x": 0, "y": 1},
                {"x": 0, "y": 2},
            ]
        }
    )


@fixture
def snake_middle_short():
    return Snake(
        **{
            "body": [
                {"x": 5, "y": 5},
                {"x": 6, "y": 5},
            ],
        }
    )


@fixture
def snake_top_middle_short():
    return Snake(
        **{
            "body": [
                {"x": 5, "y": 10},
                {"x": 6, "y": 10},
            ]
        }
    )


@fixture
def snake_bottom_middle_short():
    return Snake(
        **{
            "body": [
                {"x": 5, "y": 0},
                {"x": 6, "y": 0},
            ],
        }
    )


@fixture
def snake_left_middle_short():
    return Snake(
        **{
            "body": [
                {"x": 0, "y": 5},
                {"x": 1, "y": 5},
            ]
        }
    )


@fixture
def snake_right_middle_short():
    return Snake(
        **{
            "body": [
                {"x": 10, "y": 5},
                {"x": 9, "y": 5},
            ]
        }
    )


@fixture
def snake_top_right_short():
    return Snake(
        **{
            "body": [
                {"x": 10, "y": 10},
                {"x": 10, "y": 9},
            ]
        }
    )


@fixture
def snake_long():
    return Snake(
        **{
            "body": [
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
                {"x": 8, "y": 1},
            ]
        }
    )


@fixture
def snake_long_2():
    return Snake(
        **{
            "body": [
                {"x": 4, "y": 5},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
                {"x": 8, "y": 1},
            ],
        }
    )


@fixture
def snake_long_2_future_down_without_food():
    return Snake(
        **{
            "body": [
                {"x": 4, "y": 4},
                {"x": 4, "y": 5},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
            ]
        }
    )


@fixture
def snake_long_future_up_without_food():
    return Snake(
        **{
            "body": [
                {"x": 5, "y": 6},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
            ]
        }
    )


@fixture
def snake_long_future_right_without_food():
    return Snake(
        **{
            "body": [
                {"x": 6, "y": 5},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
            ],
        }
    )


@fixture
def snake_long_future_left_without_food():
    return Snake(
        **{
            "body": [
                {"x": 4, "y": 5},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
            ],
        }
    )
