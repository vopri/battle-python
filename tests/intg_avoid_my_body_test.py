from battle_snake.entities import NextStep, Snake
from battle_snake.interactor import MoveDecision


def test_avoid_my_body_without_food(
    sample_move_decision_with_snake_in_block_without_food: MoveDecision,
):
    sample_move_decision_with_snake_in_block_without_food._avoid_my_future_body()
    expected_moves = {NextStep.DOWN, NextStep.RIGHT}
    assert (
        set(
            sample_move_decision_with_snake_in_block_without_food.possible_moves.values()
        )
        == expected_moves
    )


def test_avoid_my_body_with_food(
    sample_move_decision_with_snake_in_block_with_food: MoveDecision,
):
    sample_move_decision_with_snake_in_block_with_food._avoid_my_future_body()
    expected_moves = {NextStep.DOWN}
    assert (
        set(sample_move_decision_with_snake_in_block_with_food.possible_moves.values())
        == expected_moves
    )
