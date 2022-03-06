import pytest
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


@pytest.mark.parametrize(
    "current_head_pos,next_step",
    [
        ((0, 10), NextStep.UP),
        ((1, 10), NextStep.UP),
        ((2, 10), NextStep.UP),
        ((3, 10), NextStep.UP),
        ((4, 10), NextStep.UP),
        ((5, 10), NextStep.UP),
        ((6, 10), NextStep.UP),
        ((7, 10), NextStep.UP),
        ((8, 10), NextStep.UP),
        ((9, 10), NextStep.UP),
        ((10, 10), NextStep.UP),
        ((0, 0), NextStep.DOWN),
        ((1, 0), NextStep.DOWN),
        ((2, 0), NextStep.DOWN),
        ((3, 0), NextStep.DOWN),
        ((4, 0), NextStep.DOWN),
        ((5, 0), NextStep.DOWN),
        ((6, 0), NextStep.DOWN),
        ((7, 0), NextStep.DOWN),
        ((8, 0), NextStep.DOWN),
        ((9, 0), NextStep.DOWN),
        ((10, 0), NextStep.DOWN),
        ((10, 0), NextStep.RIGHT),
        ((10, 1), NextStep.RIGHT),
        ((10, 2), NextStep.RIGHT),
        ((10, 3), NextStep.RIGHT),
        ((10, 4), NextStep.RIGHT),
        ((10, 5), NextStep.RIGHT),
        ((10, 6), NextStep.RIGHT),
        ((10, 7), NextStep.RIGHT),
        ((10, 8), NextStep.RIGHT),
        ((10, 9), NextStep.RIGHT),
        ((10, 10), NextStep.RIGHT),
        ((0, 0), NextStep.LEFT),
        ((0, 1), NextStep.LEFT),
        ((0, 2), NextStep.LEFT),
        ((0, 3), NextStep.LEFT),
        ((0, 4), NextStep.LEFT),
        ((0, 5), NextStep.LEFT),
        ((0, 6), NextStep.LEFT),
        ((0, 7), NextStep.LEFT),
        ((0, 8), NextStep.LEFT),
        ((0, 9), NextStep.LEFT),
        ((0, 10), NextStep.LEFT),
    ],
)
def test_multi_will_clash_with_walls(
    default_board_height_and_widht, current_head_pos, next_step
):
    walls = Walls(*default_board_height_and_widht)
    assert walls.will_clash(current_head_pos, next_step)


@pytest.mark.parametrize(
    "current_head_pos,next_step",
    [
        ((5, 9), NextStep.UP),
        ((2, 8), NextStep.DOWN),
        ((4, 9), NextStep.RIGHT),
        ((5, 10), NextStep.RIGHT),
        ((5, 1), NextStep.UP),
        ((2, 9), NextStep.UP),
    ],
)
def test_multi_will_not_clash_with_walls(
    default_board_height_and_widht, current_head_pos, next_step
):
    walls = Walls(*default_board_height_and_widht)
    assert not walls.will_clash(current_head_pos, next_step)
