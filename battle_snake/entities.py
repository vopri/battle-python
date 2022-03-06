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
        self.head: Position = self.body_incl_head[0]
        self.neck: Position = self.body_incl_head[1]

    def __len__(self):
        return len(self.body_incl_head)

    def next_theoretical_head_positions(self) -> dict[Position, NextStep]:
        result = dict()
        result[Position(self.head.x + 1, self.head.y)] = NextStep.RIGHT
        result[Position(self.head.x - 1, self.head.y)] = NextStep.LEFT
        result[Position(self.head.x, self.head.y + 1)] = NextStep.UP
        result[Position(self.head.x, self.head.y - 1)] = NextStep.DOWN
        return result


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
        if not (self.width >= pos.x >= 0):
            return True
        if not (self.height >= pos.y >= 0):
            return True
        return False
