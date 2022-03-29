import random
from typing import Dict, List

from battle_snake.entities import Board, FutureBoard, Moves, NextStep, Position, Snake


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
        self.possible_moves: Moves = self.me.get_next_theoretical_moves()
        self.future_board: FutureBoard = FutureBoard(self.board)

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
        if self._there_is_only_one_move_possible():
            return self._last_possible_next_step()
        self._exclude_dangerous_moves()
        if self._theres_no_way_to_survive():
            # don't waste time and kill yourself like a snake with honour
            return NextStep.UP
        self._select_best_possible_moves()
        return random.choice(list(self.possible_moves.values()))

    def _last_possible_next_step(self):
        return list(self.possible_moves.values())[-1]

    def _there_is_only_one_move_possible(self):
        return len(self.possible_moves) == 1

    def _exclude_impossible_moves(self):
        """Remove all possible next steps that would lead to death at once.

        This internal method doesn't include any strategies or tactis.
        The only purpose is to survive the next step.
        """
        self._avoid_walls()
        self._avoid_myself()
        self._avoid_other_snake_bodies()

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

    def _avoid_other_snake_bodies(self):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if not self.future_board.is_other_snake_body_on_this(position)
        }

    def _exclude_dangerous_moves(self, risk_tolerance=0):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if self.future_board.calc_snake_head_risk_value(position) <= 0
        }

    def _theres_no_way_to_survive(self) -> bool:
        return len(self.possible_moves) == 0

    def _select_best_possible_moves(self):
        self._lead_me_to_nearby_food()

    def _lead_me_to_nearby_food(self):
        moves_leading_to_food = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if position in self.future_board.food
        }
        if moves_leading_to_food:
            self.possible_moves = moves_leading_to_food
