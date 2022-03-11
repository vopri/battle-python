from battle_snake import interactor
from battle_snake.entities import NextStep, Position


def test_filter_walls_bottom_left(sample_board):
    possible_moves = {
        Position(-1, 0): NextStep.LEFT,
        Position(1, 0): NextStep.RIGHT,
        Position(0, 1): NextStep.UP,
        Position(0, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.RIGHT}


def test_filter_walls_bottom_right(sample_board):
    possible_moves = {
        Position(9, 0): NextStep.LEFT,
        Position(11, 0): NextStep.RIGHT,
        Position(10, 1): NextStep.UP,
        Position(10, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.LEFT}


def test_filter_walls_top_left(sample_board):
    possible_moves = {
        Position(-1, 10): NextStep.LEFT,
        Position(1, 10): NextStep.RIGHT,
        Position(0, 11): NextStep.UP,
        Position(0, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.RIGHT}


def test_filter_walls_top_right(sample_board):
    possible_moves = {
        Position(9, 10): NextStep.LEFT,
        Position(11, 10): NextStep.RIGHT,
        Position(10, 11): NextStep.UP,
        Position(10, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.LEFT}


def test_filter_walls_top_middle(sample_board):
    possible_moves = {
        Position(4, 10): NextStep.LEFT,
        Position(6, 10): NextStep.RIGHT,
        Position(5, 11): NextStep.UP,
        Position(5, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_bottom_middle(sample_board):
    possible_moves = {
        Position(4, 0): NextStep.LEFT,
        Position(6, 0): NextStep.RIGHT,
        Position(5, 1): NextStep.UP,
        Position(5, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_middle_right(sample_board):
    possible_moves = {
        Position(9, 5): NextStep.LEFT,
        Position(11, 5): NextStep.RIGHT,
        Position(10, 6): NextStep.UP,
        Position(10, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.DOWN,
    }


def test_filter_walls_middle_left(sample_board):
    possible_moves = {
        Position(-1, 5): NextStep.LEFT,
        Position(1, 5): NextStep.RIGHT,
        Position(0, 6): NextStep.UP,
        Position(0, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.RIGHT,
        NextStep.DOWN,
    }


def test_filter_walls_middle(sample_board):
    possible_moves = {
        Position(4, 5): NextStep.LEFT,
        Position(6, 5): NextStep.RIGHT,
        Position(5, 6): NextStep.UP,
        Position(5, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(sample_board, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.UP,
        NextStep.RIGHT,
    }
