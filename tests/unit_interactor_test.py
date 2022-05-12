from battle_snake.entities import NextStep, PossibleFutureBoard
from battle_snake.interactor import MyFutureHistory


def test_my_future_history_food(solo_board_2):
    hist = MyFutureHistory()
    fb = PossibleFutureBoard(solo_board_2)
    hist.save(fb)
    fb.next_turn()
    hist.save(fb)
    fb.next_turn()
    hist.save(fb)
    fb.next_turn()
    hist.save(fb)
    fb.next_turn()
    hist.save(fb)
    assert hist.get_food_after_how_many_steps(NextStep.DOWN) == 3
    assert hist.get_food_after_how_many_steps(NextStep.LEFT) == 5
    assert hist.get_food_after_how_many_steps(NextStep.UP) is None
    assert hist.get_food_after_how_many_steps(NextStep.RIGHT) is None
