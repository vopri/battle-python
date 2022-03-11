from battle_snake import interactor
from battle_snake.entities import NextStep, Snake


def test_filter_neck_left(snake_right_middle_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_right_middle_short.next_theoretical_head_positions_and_moves(),
        snake_right_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.RIGHT}
    assert set(moves.values()) == expected


def test_filter_neck_right(snake_middle_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_middle_short.next_theoretical_head_positions_and_moves(),
        snake_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_up(snake_origin: Snake):
    moves = interactor._avoid_my_neck(
        snake_origin.next_theoretical_head_positions_and_moves(),
        snake_origin,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_down(snake_top_right_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_top_right_short.next_theoretical_head_positions_and_moves(),
        snake_top_right_short,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.UP, NextStep.LEFT}
    assert set(moves.values()) == expected
