import random
from typing import Dict, List

from battle_snake.entities import Board, NextStep, Position, Snake

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""


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
    next_possible_positions: dict[
        Position, NextStep
    ] = board.my_snake.next_theoretical_head_positions()
    next_possible_positions = _filter_neck(next_possible_positions, my_snake)
    next_possible_positions = _filter_walls(board, next_possible_positions)

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(list(next_possible_positions.values()))
    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {next_possible_positions}"
    )

    return move.value


def _init_board(data):
    my_head_pos = Position(**data["you"]["head"])
    board = Board(my_head_pos, **data["board"])
    return board


def _filter_neck(next_positions, my_snake):
    return {
        position: next_step
        for position, next_step in next_positions.items()
        if position != my_snake.neck
    }


def _filter_walls(board, next_possible_positions):
    return {
        position: next_step
        for position, next_step in next_possible_positions.items()
        if not board.is_wall(position)
    }
