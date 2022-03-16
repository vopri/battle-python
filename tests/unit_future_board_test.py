from battle_snake.entities import Board


def test_board_of_future(test_board: Board):
    board = test_board.calculate_future_board()
    assert len(board.all_snakes) == 7
    assert len(test_board.all_snakes) == 4
    assert len(board.food) == 3
    assert len(test_board.food) == 4

    # for snake in test_board.all_snakes.values():
    #     print(snake)

    # print("~" * 10)
    # for snake in board.all_snakes.values():
    #     print(snake)
