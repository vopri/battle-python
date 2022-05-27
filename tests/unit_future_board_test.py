import pytest
from battle_snake.entities import (
    Board,
    GameBoardBounderies,
    NextStep,
    Position,
    PossibleFutureBoard,
    Snake,
)


def test_placeholder():
    assert True


def test_future_board_init(test_board: Board):
    future_board = PossibleFutureBoard(test_board)
    assert test_board.bounderies == future_board.bounderies
    assert future_board.food == {
        Position(2, 6),
        Position(5, 5),
        Position(5, 4),
        Position(9, 0),
    }
    assert len(test_board.food) == 4
    assert len(test_board.snakes) == 7
    assert len(future_board.possible_snakes) == 14


def test_future_board_all_possible_snakes(test_board: Board):
    future_board = PossibleFutureBoard(test_board)
    assert len(future_board.possible_snakes) == 14
    expected_heads = {
        Position(x=0, y=1),
        Position(x=1, y=6),
        Position(x=2, y=5),
        Position(x=3, y=6),
        Position(x=4, y=2),
        Position(x=4, y=4),
        Position(x=4, y=4),
        Position(x=4, y=6),
        Position(x=4, y=10),
        Position(x=5, y=5),
        Position(x=5, y=5),
        Position(x=5, y=9),
        Position(x=6, y=4),
        Position(x=9, y=10),
    }
    assert {snake.head for snake in future_board.possible_snakes} == expected_heads


def test_get_my_survived_snakes_combinations(almost_empty_board_request):
    future_board = PossibleFutureBoard(Board.from_dict(almost_empty_board_request))
    assert len(future_board.possible_snakes) == 2


def test_snake_and_future_snake_id_handover(sample_request):
    board = Board.from_dict(sample_request)
    future_board = PossibleFutureBoard(board)
    my_id = board.my_snake.id
    survivor_ids = {snake.id for snake in future_board.get_my_survived_snakes()}
    assert len(survivor_ids) == 1
    assert my_id == survivor_ids.pop()


def test_simple_future_board_several_turns():
    snake = Snake([Position(5, 5)], is_me=True)
    board = Board(GameBoardBounderies(11, 11), food={Position(4, 5)}, snakes={snake})
    future_board = PossibleFutureBoard(board)
    assert len(future_board.get_my_survived_snakes()) == 4
    assert len(future_board.food) == 1
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 12
    assert len(future_board.food) == 0


def test_complex_future_board_several_turns(test_request_move_me_3):
    board = Board.from_dict(test_request_move_me_3)
    future_board = PossibleFutureBoard(board)
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 9


def test_simple_future_board_several_turns_walls():
    snake = Snake([Position(0, 0)], is_me=True)
    board = Board(GameBoardBounderies(11, 11), food=set(), snakes={snake})
    future_board = PossibleFutureBoard(board)
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 4
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 10
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 26
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 66
