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
