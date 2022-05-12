from battle_snake.entities import NextStep, PossibleFutureBoard
from battle_snake.interactor import MyFutureHistory


def test_my_future_history_food(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    hist.save(fb)
    for _ in range(8):
        fb.next_turn()
        hist.save(fb)
    assert hist.found_food_after_how_many_steps(NextStep.DOWN) == 3
    assert hist.found_food_after_how_many_steps(NextStep.LEFT) == 5
    assert hist.found_food_after_how_many_steps(NextStep.UP) is None
    assert hist.found_food_after_how_many_steps(NextStep.RIGHT) is None


def test_my_future_history_dead_step_1(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    hist.save(fb)
    for _ in range(8):
        fb.next_turn()
        hist.save(fb)
    assert hist.all_snakes_definitely_dead_after_how_many_steps(NextStep.RIGHT) == 1


def test_my_future_history_dead_lock(solo_board_4):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_4)
    hist.save(fb)
    for _ in range(8):
        fb.next_turn()
        hist.save(fb)
    assert hist.all_snakes_definitely_dead_after_how_many_steps(NextStep.UP) == 3
