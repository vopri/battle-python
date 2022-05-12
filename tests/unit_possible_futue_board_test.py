from battle_snake.entities import PossibleFutureBoard


def test_future_board_init(solo_board_1):
    fb = PossibleFutureBoard(solo_board_1)
    assert fb.simulated_turns == 1
    assert len(fb.get_my_survived_snakes()) == 1
    fb.next_turn()
    assert fb.simulated_turns == 2
    assert len(fb.get_my_survived_snakes()) == 2
    fb.next_turn()
    assert fb.simulated_turns == 3
    assert len(fb.get_my_survived_snakes()) == 5
    fb.next_turn()
    assert fb.simulated_turns == 4
    assert len(fb.get_my_survived_snakes()) == 13
