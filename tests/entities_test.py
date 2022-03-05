from battle_snake.entities import NextStep, Walls
from pytest import fixture


@fixture
def origin():
    return (0, 0)


@fixture
def default_board_height_and_widht():
    return (11, 11)


def test_will_clash_with_walls_origin_up(origin, default_board_height_and_widht):
    walls = Walls(*default_board_height_and_widht)
    assert not walls.will_clash(origin, NextStep.UP)


def test_will_clash_with_walls_origin_right(origin, default_board_height_and_widht):
    walls = Walls(*default_board_height_and_widht)
    assert not walls.will_clash(origin, NextStep.RIGHT)


def test_will_clash_with_walls_origin_left(origin, default_board_height_and_widht):
    walls = Walls(*default_board_height_and_widht)
    assert walls.will_clash(origin, NextStep.LEFT)


def test_will_clash_with_walls_right(default_board_height_and_widht):
    walls = Walls(*default_board_height_and_widht)
    assert walls.will_clash((10, 2), NextStep.RIGHT)


def test_will_clash_with_walls_up(default_board_height_and_widht):
    walls = Walls(*default_board_height_and_widht)
    assert walls.will_clash((5, 10), NextStep.UP)
