from battle_snake import interactor
from battle_snake.entities import NextStep, Snake


def test_avoid_my_body_without_food(snake_in_block: Snake):
    possible_moves = snake_in_block.next_theoretical_head_positions_and_moves()
    filtered_moves = interactor._avoid_my_future_body(
        snake_in_block, possible_moves, my_snake_gets_food=False
    )
    expected_moves = {NextStep.DOWN, NextStep.RIGHT}
    assert set(filtered_moves.values()) == expected_moves


def test_avoid_my_body_with_food(snake_in_block: Snake):
    possible_moves = snake_in_block.next_theoretical_head_positions_and_moves()
    filtered_moves = interactor._avoid_my_future_body(
        snake_in_block, possible_moves, my_snake_gets_food=True
    )
    expected_moves = {NextStep.DOWN}
    assert set(filtered_moves.values()) == expected_moves
