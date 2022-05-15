from battle_snake.entities import NextStep, PossibleFutureBoard
from battle_snake.interactor import MyFutureHistory, Tactics


def test_my_future_history_food(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    hist.save(fb)
    for _ in range(8):
        fb.next_turn()
        hist.save(fb)
    assert hist.my_snake_found_food_after_how_many_steps(NextStep.DOWN) == 3
    assert hist.my_snake_found_food_after_how_many_steps(NextStep.LEFT) == 5
    assert hist.my_snake_found_food_after_how_many_steps(NextStep.UP) is None
    assert hist.my_snake_found_food_after_how_many_steps(NextStep.RIGHT) is None


def test_my_future_history_dead_step_1(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    assert hist.all_my_snakes_definitely_dead_after_how_many_steps(NextStep.RIGHT) == 1


def test_my_future_history_dead_lock(solo_board_4):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_4)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    assert hist.all_my_snakes_definitely_dead_after_how_many_steps(NextStep.UP) == 3


def test_tactis(solo_board_4):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_4)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    tactics = Tactics(hist)
    assert tactics.decide() == NextStep.DOWN


def test_tactis_2(solo_board_3):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_3)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    tactics = Tactics(hist)
    assert tactics.decide() in (NextStep.DOWN, NextStep.LEFT)


def test_tactis_3(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    tactics = Tactics(hist)
    assert tactics.decide() == NextStep.DOWN


def test_tactis_4(solo_board_1):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_1)
    fb.register_recorder(hist)
    for _ in range(8):
        fb.next_turn()
    tactics = Tactics(hist)
    assert tactics.decide() == NextStep.UP
