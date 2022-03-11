import json
from pathlib import Path

from battle_snake.entities import Board, Position
from pytest import fixture


@fixture(scope="session")
def sample_request():
    sample_request = Path.cwd() / "tests" / "sample_request.json"
    return json.loads(sample_request.read_text())


@fixture
def sample_board(sample_request):
    return Board(
        Position(**sample_request["you"]["head"]),
        **sample_request["board"],
    )


@fixture
def sample_board_data(sample_request) -> dict:
    return sample_request["board"]
