import json
from pathlib import Path

from battle_snake.entities import Board, Position
from pytest import fixture


@fixture
def move_request_head_origin():
    move_request_1 = Path.cwd() / "tests" / "move_request_head_origin.json"
    return json.loads(move_request_1.read_text())


@fixture
def board_from_file(move_request_head_origin):
    return Board(
        Position(**move_request_head_origin["you"]["head"]),
        **move_request_head_origin["board"]
    )


@fixture
def board_data_two() -> dict:
    return {
        "height": 11,
        "width": 11,
        "food": [{"x": 5, "y": 5}, {"x": 9, "y": 0}, {"x": 2, "y": 6}],
        "hazards": [{"x": 3, "y": 2}],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 54,
                "body": [
                    {"x": 0, "y": 1},
                    {"x": 0, "y": 0},
                    {"x": 1, "y": 0},
                    {"x": 2, "y": 0},
                ],
                "latency": "111",
                "head": {"x": 0, "y": 1},
                "length": 4,
                "shout": "why are we shouting??",
                "squad": "",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel",
                },
            },
            {
                "id": "snake-b67f4906-94ae-11ea-bb37",
                "name": "Another Snake",
                "health": 16,
                "body": [
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 4},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                ],
                "latency": "222",
                "head": {"x": 5, "y": 5},
                "length": 4,
                "shout": "I'm not really sure...",
                "squad": "",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled",
                },
            },
        ],
    }


@fixture
def board_data() -> dict:
    return {
        "height": 11,
        "width": 11,
        "food": [{"x": 5, "y": 5}, {"x": 9, "y": 0}, {"x": 2, "y": 6}],
        "hazards": [{"x": 3, "y": 2}],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 54,
                "body": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}],
                "latency": "111",
                "head": {"x": 0, "y": 0},
                "length": 3,
                "shout": "why are we shouting??",
                "squad": "",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel",
                },
            },
            {
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
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled",
                },
            },
        ],
    }
