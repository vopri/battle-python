from battle_snake.entities import Board, NextStep, Position, Snake


def test_postion_init():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos.x == 3
    assert pos.y == 2


def test_postion_equal():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos == Position(3, 2)


def test_snake_init(snake_data):
    snake = Snake(**snake_data)
    assert snake.head == Position(5, 4)
    assert snake.body_incl_head == [
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(6, 2),
    ]
    assert snake.neck == Position(5, 3)
    assert snake.tail == Position(6, 2)
    assert len(snake) == 4


def test_next_theoretical_positions(snake):
    assert snake.head == Position(5, 4)
    assert snake.next_theoretical_head_positions_and_moves() == {
        Position(6, 4): NextStep.RIGHT,
        Position(4, 4): NextStep.LEFT,
        Position(5, 5): NextStep.UP,
        Position(5, 3): NextStep.DOWN,
    }


def test_board_init(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    assert board.height == 11
    assert board.width == 11
    assert board.food == {
        Position(5, 5),
        Position(9, 0),
        Position(2, 6),
    }
    assert len(board.all_snakes) == 2
    snake_on_5_4 = board.all_snakes.get(Position(5, 4))
    assert len(snake_on_5_4) == 4  # type: ignore
    assert snake_on_5_4.body_incl_head[-1] == Position(6, 2)  # type: ignore


def test_get_my_snake(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    me = board.my_snake
    assert len(me) == 3
    assert me.neck == Position(1, 0)


def test_is_wall(board_data):
    board = Board(my_head=Position(0, 0), **board_data)
    assert not board.is_wall(Position(0, 0))
    assert not board.is_wall(Position(3, 3))
    assert not board.is_wall(Position(10, 10))
    assert not board.is_wall(Position(0, 10))
    assert not board.is_wall(Position(10, 0))
    assert board.is_wall(Position(-1, 3))
    assert board.is_wall(Position(2, -3))
    assert board.is_wall(Position(11, 3))
    assert board.is_wall(Position(5, 11))
    assert board.is_wall(Position(15, 15))
    assert board.is_wall(Position(-3, 15))
    assert board.is_wall(Position(-3, -8))
