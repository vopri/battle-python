import random
from typing import Dict, List

from battle_snake.entities import Board, NextStep, Position, Snake

Moves = dict[Position, NextStep]  # type alias


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author.
    For customization options, see https://docs.battlesnake.com/references/personalization
    """
    return {
        "apiversion": "1",
        "author": "vopri",
        "color": "#ff9900",
        "head": "fang",
        "tail": "hook",
    }


class MoveDecision:
    """Decision make for the next move of my snake. Entry point is method 'decide'"""

    def __init__(self, data: dict):
        self.board: Board = self._init_board(data)
        self.possible_moves: Moves = self.me.next_theoretical_head_positions_and_moves()

    @property
    def me(self) -> Snake:
        """Shortcut to my snake"""
        return self.board.my_snake

    def _init_board(self, data: dict) -> Board:
        my_head_pos = Position(**data["you"]["head"])
        return Board(my_head_pos, **data["board"])

    def decide(self) -> NextStep:
        """Entry point to find the next move of my snake

        Returns:
            NextStep: Concrete next step of my snake
        """
        self._exclude_impossible_moves()
        return random.choice(list(self.possible_moves.values()))

    def _exclude_impossible_moves(self):
        """Remove all possible next steps that would lead to death at once.

        This internal method doesn't include any strategies or tactis.
        The only purpose is to survive the next step.
        """
        self._avoid_walls()
        self._avoid_myself()

    def _avoid_walls(self):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if not self.board.is_wall(position)
        }

    def _avoid_myself(self):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if not self.me.will_bite_itself(next_step, self._is_food_available())
        }

    def _is_food_available(self):
        return self.me.head in self.board.food
