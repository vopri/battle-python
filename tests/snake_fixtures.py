from battle_snake.entities import Snake
from pytest import fixture


@fixture
def snake(snake_data) -> Snake:
    return Snake(**snake_data)


@fixture
def snake_data() -> dict:
    return {
        "id": "snake-b67f4906-94ae-11ea-bb37",
        "name": "Another Snake",
        "health": 16,
        "body": [
            {"x": 5, "y": 4},
            {"x": 5, "y": 3},
            {"x": 6, "y": 3},
            {"x": 6, "y": 2},
        ],
        "latency": "222",
        "head": {"x": 5, "y": 4},
        "length": 4,
        "shout": "I'm not really sure...",
        "squad": "",
        "customizations": {"color": "#26CF04", "head": "silly", "tail": "curled"},
    }


@fixture
def snake_in_block():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 7, "y": 4},
                {"x": 6, "y": 4},
                {"x": 6, "y": 5},
                {"x": 7, "y": 5},
                {"x": 8, "y": 5},
                {"x": 8, "y": 4},
            ],
            "latency": "111",
            "head": {"x": 7, "y": 4},
            "length": 6,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_origin():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 0, "y": 0}, {"x": 0, "y": 1}, {"x": 0, "y": 2}],
            "latency": "111",
            "head": {"x": 0, "y": 0},
            "length": 3,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_middle_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 5, "y": 5}, {"x": 6, "y": 5}],
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_top_middle_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 5, "y": 10}, {"x": 6, "y": 10}],
            "latency": "111",
            "head": {"x": 5, "y": 10},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_bottom_middle_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 5, "y": 0}, {"x": 6, "y": 0}],
            "latency": "111",
            "head": {"x": 5, "y": 0},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_left_middle_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 0, "y": 5}, {"x": 1, "y": 5}],
            "latency": "111",
            "head": {"x": 0, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_right_middle_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 10, "y": 5}, {"x": 9, "y": 5}],
            "latency": "111",
            "head": {"x": 10, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_top_right_short():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [{"x": 10, "y": 10}, {"x": 10, "y": 9}],
            "latency": "111",
            "head": {"x": 10, "y": 10},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
                {"x": 8, "y": 1},
            ],
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long_2():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
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
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long_2_future_down_without_food():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
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
            ],
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long_future_up_without_food():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 5, "y": 6},
                {"x": 5, "y": 5},
                {"x": 5, "y": 4},
                {"x": 5, "y": 3},
                {"x": 6, "y": 3},
                {"x": 7, "y": 3},
                {"x": 7, "y": 2},
                {"x": 8, "y": 2},
            ],
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long_future_right_without_food():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
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
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )


@fixture
def snake_long_future_left_without_food():
    return Snake(
        **{
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
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
            "latency": "111",
            "head": {"x": 5, "y": 5},
            "length": 2,
            "shout": "why are we shouting??",
            "squad": "",
            "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
        }
    )
