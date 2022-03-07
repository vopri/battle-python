import copy
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class NextStep(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class Snake:
    def __init__(self, **snake_data: dict):
        self.body_incl_head: list[Position] = [
            Position(**position) for position in snake_data["body"]
        ]

    @property
    def head(self) -> Position:
        return self.body_incl_head[0]

    @property
    def neck(self) -> Position:
        return self.body_incl_head[1]

    @property
    def tail(self) -> Position:
        return self.body_incl_head[-1]

    def __len__(self):
        return len(self.body_incl_head)

    def next_theoretical_head_positions_and_moves(self) -> dict[Position, NextStep]:
        result = dict()
        result[Position(self.head.x + 1, self.head.y)] = NextStep.RIGHT
        result[Position(self.head.x - 1, self.head.y)] = NextStep.LEFT
        result[Position(self.head.x, self.head.y + 1)] = NextStep.UP
        result[Position(self.head.x, self.head.y - 1)] = NextStep.DOWN
        return result

    def calculate_future_snake(self, next_step: NextStep, food: bool = False):
        future_snake = copy.deepcopy(self)
        future_head_position: Position = self._calc_future_head_position(next_step)
        self._add_future_head_to_future_snake(future_snake, future_head_position)
        if not food:
            self._remove_tail(future_snake)
        return future_snake

    def _add_future_head_to_future_snake(self, future_snake, future_head_position):
        future_snake.body_incl_head.insert(0, future_head_position)

    def _calc_future_head_position(self, next_step):
        return [
            position
            for position, n_step in self.next_theoretical_head_positions_and_moves().items()
            if n_step == next_step
        ][0]

    def _remove_tail(self, future_snake):
        future_snake.body_incl_head.pop()


class Board:
    def __init__(self, my_head: Position, **board_data: dict):
        self.height: int = board_data["height"]  # type: ignore
        self.width: int = board_data["width"]  # type: ignore
        self.food: set[Position] = {
            Position(**position_data) for position_data in board_data["food"]
        }
        self.all_snakes: dict[Position, Snake] = {
            Position(**snake_data["head"]): Snake(**snake_data)
            for snake_data in board_data["snakes"]
        }
        self.my_head: Position = my_head

    @property
    def my_snake(self) -> Snake:
        return self.all_snakes[self.my_head]

    def is_wall(self, pos: Position) -> bool:
        if pos.x < 0 or pos.y < 0:
            return True
        if pos.x >= self.width:
            return True
        if pos.y >= self.height:
            return True
        return False
