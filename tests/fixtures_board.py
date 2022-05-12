import json
from pathlib import Path

from battle_snake.entities import Board, Position, Snake
from pytest import fixture


@fixture(scope="session")
def sample_request():
    sample_request = Path.cwd() / "tests" / "sample_request.json"
    return json.loads(sample_request.read_text())


@fixture(scope="session")
def almost_empty_board_request():
    sample_request = Path.cwd() / "tests" / "almost_empty_board_request.json"
    return json.loads(sample_request.read_text())


@fixture
def sample_board(sample_request):
    return Board.from_dict(sample_request)


@fixture
def sample_board_data(sample_request) -> dict:
    return sample_request["board"]


@fixture()
def test_request():
    sample_request = Path.cwd() / "tests" / "test_request.json"
    return json.loads(sample_request.read_text())


@fixture()
def test_request_move_me_1():
    sample_request = Path.cwd() / "tests" / "test_request_move_me_1.json"
    return json.loads(sample_request.read_text())


@fixture()
def test_request_move_me_2():
    sample_request = Path.cwd() / "tests" / "test_request_move_me_2.json"
    return json.loads(sample_request.read_text())


@fixture
def sample_board_move_me_2(test_request_move_me_2) -> Board:
    return Board.from_dict(test_request_move_me_2)


@fixture()
def test_request_move_me_3():
    sample_request = Path.cwd() / "tests" / "test_request_move_me_3.json"
    return json.loads(sample_request.read_text())


@fixture
def sample_board_move_me_3(test_request_move_me_3) -> Board:
    return Board.from_dict(test_request_move_me_3)


@fixture()
def test_request_move_me_4():
    sample_request = Path.cwd() / "tests" / "test_request_move_me_4.json"
    return json.loads(sample_request.read_text())


@fixture
def test_board(test_request):
    return Board.from_dict(test_request)


@fixture()
def solo_board_request_1():
    sample_request = Path.cwd() / "tests" / "solo_board_1.json"
    return json.loads(sample_request.read_text())


@fixture
def solo_board_1(solo_board_request_1) -> Board:
    return Board.from_dict(solo_board_request_1)


@fixture()
def solo_board_request_2():
    sample_request = Path.cwd() / "tests" / "solo_board_2.json"
    return json.loads(sample_request.read_text())


@fixture
def solo_board_2(solo_board_request_2) -> Board:
    return Board.from_dict(solo_board_request_2)


@fixture()
def solo_board_request_3():
    sample_request = Path.cwd() / "tests" / "solo_board_3.json"
    return json.loads(sample_request.read_text())


@fixture
def solo_board_3(solo_board_request_3) -> Board:
    return Board.from_dict(solo_board_request_3)


@fixture()
def solo_board_request_4():
    sample_request = Path.cwd() / "tests" / "solo_board_4.json"
    return json.loads(sample_request.read_text())


@fixture
def solo_board_4(solo_board_request_4) -> Board:
    return Board.from_dict(solo_board_request_4)
