from battle_snake.entities import Board, Position


def test_board_of_future(test_board: Board):
    board = test_board.calculate_future_board()
    assert len(test_board.food) == 4
    assert len(board.food) == 2
    assert len(test_board.all_snakes) == 7
    future_heads = (
        Position(x=5, y=5),
        Position(x=6, y=4),
        Position(x=4, y=4),
        # Position(x=5, y=11), # wall
        Position(x=5, y=9),
        Position(x=4, y=10),
        # Position(x=5, y=3), # killed
        Position(x=6, y=2),  # FIXME: should have been killed, too!
        Position(x=4, y=2),
        Position(x=2, y=5),
        Position(x=3, y=6),
        Position(x=1, y=6),
        Position(x=4, y=6),
        # Position(x=10, y=11), # wall
        # Position(x=11, y=10), # wall
        Position(x=9, y=10),
    )
    for snake in board.all_snakes.values():
        assert snake.head in future_heads

    for snake in board.all_snakes.values():
        print(snake.head)
