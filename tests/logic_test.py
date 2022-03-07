import json
from pathlib import Path

import pytest
from battle_snake import logic
from battle_snake.entities import Board, NextStep, Position, Snake
from flask import request
from pytest import fixture


@fixture
def move_request_head_origin():
    move_request_1 = Path.cwd() / "tests" / "move_request_head_origin.json"
    return json.loads(move_request_1.read_text())


@fixture
def board(move_request_head_origin):
    return Board(
        Position(**move_request_head_origin["you"]["head"]),
        **move_request_head_origin["board"]
    )


def test_filter_walls_bottom_left(board):
    possible_moves = {
        Position(-1, 0): NextStep.LEFT,
        Position(1, 0): NextStep.RIGHT,
        Position(0, 1): NextStep.UP,
        Position(0, -1): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.RIGHT}


def test_filter_walls_bottom_right(board):
    possible_moves = {
        Position(9, 0): NextStep.LEFT,
        Position(11, 0): NextStep.RIGHT,
        Position(10, 1): NextStep.UP,
        Position(10, -1): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.LEFT}


def test_filter_walls_top_left(board):
    possible_moves = {
        Position(-1, 10): NextStep.LEFT,
        Position(1, 10): NextStep.RIGHT,
        Position(0, 11): NextStep.UP,
        Position(0, 9): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.RIGHT}


def test_filter_walls_top_right(board):
    possible_moves = {
        Position(9, 10): NextStep.LEFT,
        Position(11, 10): NextStep.RIGHT,
        Position(10, 11): NextStep.UP,
        Position(10, 9): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.LEFT}


def test_filter_walls_top_middle(board):
    possible_moves = {
        Position(4, 10): NextStep.LEFT,
        Position(6, 10): NextStep.RIGHT,
        Position(5, 11): NextStep.UP,
        Position(5, 9): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_bottom_middle(board):
    possible_moves = {
        Position(4, 0): NextStep.LEFT,
        Position(6, 0): NextStep.RIGHT,
        Position(5, 1): NextStep.UP,
        Position(5, -1): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_middle_right(board):
    possible_moves = {
        Position(9, 5): NextStep.LEFT,
        Position(11, 5): NextStep.RIGHT,
        Position(10, 6): NextStep.UP,
        Position(10, 4): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.DOWN,
    }


def test_filter_walls_middle_left(board):
    possible_moves = {
        Position(-1, 5): NextStep.LEFT,
        Position(1, 5): NextStep.RIGHT,
        Position(0, 6): NextStep.UP,
        Position(0, 4): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.RIGHT,
        NextStep.DOWN,
    }


def test_filter_walls_middle(board):
    possible_moves = {
        Position(4, 5): NextStep.LEFT,
        Position(6, 5): NextStep.RIGHT,
        Position(5, 6): NextStep.UP,
        Position(5, 4): NextStep.DOWN,
    }
    filtered_moves = logic._filter_walls(board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.UP,
        NextStep.RIGHT,
    }


def test_filter_neck_left(snake_right_middle_short: Snake):
    moves = logic._filter_neck(
        snake_right_middle_short.next_theoretical_head_positions_and_moves(),
        snake_right_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.RIGHT}
    assert set(moves.values()) == expected


def test_filter_neck_right(snake_middle_short: Snake):
    moves = logic._filter_neck(
        snake_middle_short.next_theoretical_head_positions_and_moves(),
        snake_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_up(snake_origin: Snake):
    moves = logic._filter_neck(
        snake_origin.next_theoretical_head_positions_and_moves(),
        snake_origin,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_down(snake_top_right_short: Snake):
    moves = logic._filter_neck(
        snake_top_right_short.next_theoretical_head_positions_and_moves(),
        snake_top_right_short,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.UP, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_right_without_food.body_incl_head
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_left_without_food.body_incl_head
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, food=False
    )
    assert (
        future_snake.body_incl_head == snake_long_future_up_without_food.body_incl_head
    )


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_2_future_down_without_food.body_incl_head
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
