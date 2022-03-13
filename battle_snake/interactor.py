import random
from typing import Dict, List

from battle_snake.entities import Board, NextStep, Position, Snake

Moves = dict[Position, NextStep]  # type alias


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


class MoveDecision:
    def __init__(self, data: dict):
        self.board: Board = self._init_board(data)
        self.possible_moves: Moves = self.me.next_theoretical_head_positions_and_moves()

    @property
    def me(self) -> Snake:
        return self.board.my_snake

    def _init_board(self, data: dict) -> Board:
        my_head_pos = Position(**data["you"]["head"])
        return Board(my_head_pos, **data["board"])

    def decide(self) -> NextStep:
        self._exclude_impossible_moves()
        return random.choice(list(self.possible_moves.values()))

    def _exclude_impossible_moves(self):
        self._avoid_walls()
        self._avoid_my_neck()
        self._avoid_my_future_body()

    def _avoid_walls(self):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if not self.board.is_wall(position)
        }

    def _avoid_my_neck(self):
        self.possible_moves = {
            position: next_step
            for position, next_step in self.possible_moves.items()
            if position != self.me.neck
        }

    def _avoid_my_future_body(self):
        save_moves = {}
        for position, next_step in self.possible_moves.items():
            possible_future_snake = self.me.calculate_future_snake(
                next_step, self._is_food_available()
            )
            possible_future_body_without_head = possible_future_snake.body_incl_head[1:]
            i_will_bite_myself = (
                possible_future_snake.head in possible_future_body_without_head
            )
            if not i_will_bite_myself:
                save_moves[position] = next_step
        self.possible_moves = save_moves

    def _is_food_available(self):
        return self.me.head in self.board.food
