import random
from typing import Dict, List

from battle_snake.entities import Board, NextStep, Position, Snake

"""
This file can be a nice home for your Battlesnake's interactor and helper functions.

We have started this for you, and included some interactor to remove your Battlesnake's 'neck'
from the list of possible moves!
"""
Moves = dict[Position, NextStep]  # type aliase


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "vopri",
        "color": "#ff9900",
        "head": "fang",
        "tail": "hook",
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".
    """
    board: Board = _init_board(data)
    my_snake: Snake = board.my_snake
    next_possible_moves: Moves = (
        board.my_snake.next_theoretical_head_positions_and_moves()
    )
    next_possible_moves = _avoid_my_neck(next_possible_moves, my_snake)
    next_possible_moves = _avoid_walls(board, next_possible_moves)
    my_snake_gets_food = _is_food_available(board, my_snake)
    next_possible_moves = _avoid_my_future_body(
        my_snake, next_possible_moves, my_snake_gets_food
    )

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(list(next_possible_moves.values()))
    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {next_possible_moves}"
    )

    return move.value


def _init_board(data):
    my_head_pos = Position(**data["you"]["head"])
    board = Board(my_head_pos, **data["board"])
    return board


def _avoid_my_neck(next_possible_moves: Moves, my_snake: Snake):
    return {
        position: next_step
        for position, next_step in next_possible_moves.items()
        if position != my_snake.neck
    }


def _avoid_walls(board: Board, next_possible_moves: Moves):
    return {
        position: next_step
        for position, next_step in next_possible_moves.items()
        if not board.is_wall(position)
    }


def _avoid_my_future_body(
    my_snake: Snake,
    next_possible_moves: Moves,
    my_snake_gets_food: bool,
) -> Moves:
    save_moves = {}
    for position, next_step in next_possible_moves.items():
        possible_future_snake = my_snake.calculate_future_snake(
            next_step, my_snake_gets_food
        )
        possible_future_body_without_head = possible_future_snake.body_incl_head[1:]
        i_will_bite_myself = (
            possible_future_snake.head in possible_future_body_without_head
        )
        if not i_will_bite_myself:
            save_moves[position] = next_step
    return save_moves


def _is_food_available(board, my_snake):
    return my_snake.head in board.food
