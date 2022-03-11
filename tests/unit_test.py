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


def test_snake_init(sample_snake_data):
    snake = Snake(**sample_snake_data)
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


def test_next_theoretical_positions(sample_snake):
    assert sample_snake.head == Position(5, 4)
    assert sample_snake.next_theoretical_head_positions_and_moves() == {
        Position(6, 4): NextStep.RIGHT,
        Position(4, 4): NextStep.LEFT,
        Position(5, 5): NextStep.UP,
        Position(5, 3): NextStep.DOWN,
    }


def test_board_init(sample_board_data):
    my_head = Position(0, 0)
    board = Board(
        my_head=my_head,
        **sample_board_data,
    )
    assert board.height == 11
    assert board.width == 11
    assert board.food == {
        Position(5, 5),
        Position(9, 0),
        Position(2, 6),
    }
    assert len(board.all_snakes) == 2
    snake = board.all_snakes.get(Position(5, 4))
    assert len(snake) == 4  # type: ignore
    assert snake.body_incl_head[-1] == Position(6, 2)  # type: ignore
    assert snake.tail == Position(6, 2)  # type: ignore


def test_get_my_snake(sample_board):
    me = sample_board.my_snake
    assert len(me) == 3
    assert me.neck == Position(1, 0)
    assert me.tail == Position(2, 0)


def test_is_wall(sample_board):
    assert not sample_board.is_wall(Position(0, 0))
    assert not sample_board.is_wall(Position(3, 3))
    assert not sample_board.is_wall(Position(10, 10))
    assert not sample_board.is_wall(Position(0, 10))
    assert not sample_board.is_wall(Position(10, 0))
    assert sample_board.is_wall(Position(-1, 3))
    assert sample_board.is_wall(Position(2, -3))
    assert sample_board.is_wall(Position(11, 3))
    assert sample_board.is_wall(Position(5, 11))
    assert sample_board.is_wall(Position(15, 15))
    assert sample_board.is_wall(Position(-3, 15))
    assert sample_board.is_wall(Position(-3, -8))