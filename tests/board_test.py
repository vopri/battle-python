import pytest
from battle_snake.entities import Position, Snake


def test_postion_init():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos.x == 3
    assert pos.y == 2


def test_postion_equal():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos == Position(3, 2)


def test_snake_init(snake_data):
    snake = Snake(**snake_data)
    assert snake.head == Position(5, 4)
    assert snake.body == [
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(6, 2),
    ]


@pytest.fixture
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
