from battle_snake.entities import Snake
from battle_snake.interactor import MoveDecision
from pytest import fixture


@fixture
def sample_move_decision(sample_request: dict):
    return MoveDecision(sample_request)


@fixture
def sample_move_decision_with_snake_in_block_without_food(
    sample_request: dict, snake_in_block: Snake
):
    md = MoveDecision(sample_request)
    md.board.snakes = {snake_in_block}
    md.board.my_snake.head = snake_in_block.head  # type: ignore
    return md


@fixture
def sample_move_decision_with_snake_in_block_with_food(
    sample_request: dict, snake_in_block: Snake
):
    md = MoveDecision(sample_request)
    md.board.snakes = {snake_in_block}
    md.board.my_snake.head = snake_in_block.head  # type: ignore
    md.board.food.add(snake_in_block.head)
    return md
