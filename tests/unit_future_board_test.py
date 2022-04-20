import pytest
from battle_snake.entities import (
    Board,
    FutureBoard,
    GameBoardBounderies,
    NextStep,
    Position,
    Snake,
)


def test_future_board_init(test_board: Board):
    future_board = FutureBoard(test_board)
    assert test_board.bounderies == future_board.bounderies
    assert future_board.food == {
        Position(5, 5),
        Position(9, 0),
    }
    assert len(test_board.food) == 4
    assert len(future_board.food) == 2
    assert len(test_board.snakes) == 7


def test_future_board_all_possible_snakes(test_board: Board):
    future_board = FutureBoard(test_board)
    assert len(future_board.all_possible_snakes) == 14
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
    assert {snake.head for snake in future_board.all_possible_snakes} == expected_heads


@pytest.mark.parametrize(
    "board_name, risk_tolerance, amount_of_my_survived_snakes_under_risk_tolerance",
    [
        ("test_board", 1, 1),
        ("test_board", 0.5, 1),
        ("sample_board_move_me_1", 1, 1),
        ("sample_board_move_me_1", 0, 0),
        ("sample_board_move_me_1", 0.5, 1),
        ("sample_board_move_me_1", 0.3, 0),
        ("sample_board_move_me_2", 1, 3),
        ("sample_board_move_me_2", 0, 1),
        ("sample_board_move_me_2", 0.30, 1),
        ("sample_board_move_me_2", 0.40, 3),
        ("sample_board_move_me_2", 0.7, 3),
    ],
)
def test_get_my_survived_snakes(
    board_name: str,
    risk_tolerance: float,
    amount_of_my_survived_snakes_under_risk_tolerance: int,
    request: pytest.FixtureRequest,
):
    board = request.getfixturevalue(board_name)
    future_board = FutureBoard(board)
    snakes = [
        snake
        for snake in future_board.get_my_survived_snakes()
        if snake.head_collision_risk <= risk_tolerance
    ]
    assert len(snakes) == amount_of_my_survived_snakes_under_risk_tolerance


def test_get_my_survived_snakes_combinations(almost_empty_board_request):
    future_board = FutureBoard(Board.from_dict(almost_empty_board_request))
    assert len(future_board.all_possible_snakes) == 2


def test_snake_and_future_snake_id_handover(sample_request):
    board = Board.from_dict(sample_request)
    future_board = FutureBoard(board)
    my_id = board.my_snake.id
    survivor_ids = {snake.id for snake in future_board.get_my_survived_snakes()}
    assert len(survivor_ids) == 1
    assert my_id == survivor_ids.pop()


def test_find_variants_of_snake(test_request_move_me_3):
    board = Board.from_dict(test_request_move_me_3)
    future_board = FutureBoard(board)
    future_snakes = list(future_board.get_my_survived_snakes())
    one_future_snake = future_snakes[0]
    future_variants = future_board._get_variants_of(one_future_snake)
    assert future_variants == set(future_snakes)


# param: id + head, risk
@pytest.mark.parametrize(
    "id, head, expected_risk_value",
    [
        (Position(4, 5), Position(5, 5), 1 / 3),
        (Position(4, 5), Position(4, 6), 0),
        (Position(5, 4), Position(5, 5), 0),  # I'm bigger!
        (Position(4, 5), Position(4, 4), 1 / 3),
    ],
)
def test_calc_head_collision_risk(
    test_request_move_me_3, id, head, expected_risk_value
):
    board = Board.from_dict(test_request_move_me_3)
    future_board = FutureBoard(board)
    future_snakes = [
        snake
        for snake in future_board.all_possible_snakes
        if snake.id == id and snake.head == head
    ]
    assert len(future_snakes) == 1
    f_snake = future_snakes[0]
    assert future_board._calc_head_collision_risk_for(f_snake) == expected_risk_value


def test_future_snake_head_collision_risk(test_request_move_me_3):
    board = Board.from_dict(test_request_move_me_3)
    future_board = FutureBoard(board)
    for snake in future_board.all_possible_snakes:
        assert snake.head_collision_risk >= 0
    future_snakes = [
        snake
        for snake in future_board.all_possible_snakes
        if snake.id == Position(4, 5) and snake.head == Position(5, 5)
    ]
    assert len(future_snakes) == 1
    f_snake = future_snakes[0]
    assert f_snake.head_collision_risk == 1 / 3


def test_remove_future_snake_head_collision_risk(test_request_move_me_4):
    board = Board.from_dict(test_request_move_me_4)
    future_board = FutureBoard(board)
    future_snakes = [
        snake
        for snake in future_board.all_possible_snakes
        if snake.id == Position(3, 2)
    ]
    assert len(future_snakes) == 0
    future_snakes = [
        snake
        for snake in future_board.all_possible_snakes
        if snake.id == Position(5, 2)
    ]
    assert len(future_snakes) == 1
    f_snake = future_snakes[0]
    assert f_snake.head_collision_risk == 0


def test_simple_future_board_several_turns():
    snake = Snake([Position(5, 5)], is_me=True)
    board = Board(GameBoardBounderies(11, 11), food={Position(4, 5)}, snakes={snake})
    future_board = FutureBoard(board)
    assert len(future_board.get_my_survived_snakes()) == 4
    assert len(future_board.food) == 1
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 12
    assert len(future_board.food) == 0
    for snake in future_board.get_my_survived_snakes():
        assert snake.head_collision_risk == 0


def test_complex_future_board_several_turns(test_request_move_me_3):
    board = Board.from_dict(test_request_move_me_3)
    future_board = FutureBoard(board)
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 9


def test_simple_future_board_several_turns_walls():
    snake = Snake([Position(0, 0)], is_me=True)
    board = Board(GameBoardBounderies(11, 11), food=set(), snakes={snake})
    future_board = FutureBoard(board)
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 4
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 8
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 16
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 32


def test_simple_future_board_several_turns_biting():
    snake = Snake([Position(0, 0)], is_me=True)
    other_snake = Snake([Position(2, 0)], is_me=False)
    board = Board(GameBoardBounderies(11, 11), food=set(), snakes={snake, other_snake})
    future_board = FutureBoard(board)
    interesting_snake = [
        snake
        for snake in future_board.get_my_survived_snakes()
        if snake.head == Position(1, 0)
    ][0]
    assert interesting_snake.head_collision_risk == 1 / 3
    future_board.next_turn()
    assert len(future_board.get_my_survived_snakes()) == 3
