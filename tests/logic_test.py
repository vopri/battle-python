import json
from pathlib import Path

import pytest
from battle_snake import logic
from battle_snake.entities import NextStep
from pytest import fixture


@fixture
def move_request_head_origin():
    move_request_1 = Path.cwd() / "tests" / "move_request_head_origin.json"
    return json.loads(move_request_1.read_text())


@pytest.mark.repeat(100)
def test_path(move_request_head_origin):
    chosen_move = logic.choose_move(move_request_head_origin)
    assert chosen_move != NextStep.DOWN.value
    assert chosen_move != NextStep.LEFT.value


@fixture
def snake_origin():
    return {
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


@fixture
def snake_middle_short():
    return {
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


@fixture
def snake_top_middle_short():
    return {
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


@fixture
def snake_bottom_middle_short():
    return {
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


@fixture
def snake_left_middle_short():
    return {
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


@fixture
def snake_right_middle_short():
    return {
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


@fixture
def snake_top_right_short():
    return {
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
