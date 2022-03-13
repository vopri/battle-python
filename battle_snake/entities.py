import copy
from dataclasses import dataclass
from enum import Enum
from itertools import groupby
from operator import attrgetter
from typing import Optional
from unittest.util import sorted_list_difference


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
    def body_without_head(self) -> list[Position]:
        return self.body_incl_head[1:]

    @property
    def neck(self) -> Position:
        return self.body_incl_head[1]

    @property
    def tail(self) -> Position:
        return self.body_incl_head[-1]

    def __len__(self):
        return len(self.body_incl_head)

    def __str__(self):
        """Visualize snake in 11 x 11 field"""
        field = self._init_field()
        convert_row = lambda row: "".join([cell for cell in row])
        for pos in self.body_incl_head:
            self._enter_snake_into_field(field, pos)
        self._paint_field_walls(field)
        return "\n".join(convert_row(row) for row in field)

    def _init_field(self):
        field: list[list[str]] = [["·" for i in range(11)] for j in range(11)]
        return field

    def _enter_snake_into_field(self, field, pos):
        char = "x"
        if pos == self.head:
            char = "o"
        field[10 - pos.y][pos.x] = char

    def _paint_field_walls(self, field):
        field.insert(0, ["=" for i in range(11)])
        field.append(["=" for i in range(11)])
        for row in field:
            row.insert(0, "|")
            row.append("|")

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
