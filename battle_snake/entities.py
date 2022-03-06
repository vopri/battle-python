from dataclasses import dataclass
from enum import Enum


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
        self.head: Position = Position(**snake_data["head"])
        self.body: list[Position] = [
            Position(**position) for position in snake_data["body"]
        ]

    def next_theoretical_positions(self) -> dict[Position, NextStep]:
        result = dict()
        result[Position(self.head.x + 1, self.head.y)] = NextStep.RIGHT
        result[Position(self.head.x - 1, self.head.y)] = NextStep.LEFT
        result[Position(self.head.x, self.head.y + 1)] = NextStep.UP
        result[Position(self.head.x, self.head.y - 1)] = NextStep.DOWN
        return result


class Walls:
    def __init__(self, board_height: int, board_width: int):
        self.board_height = board_height
        self.board_width = board_width

    def will_clash(
        self, current_head_pos: tuple[int, int], next_step: NextStep
    ) -> bool:
        if self._head_on_left_boarder(current_head_pos) and next_step == NextStep.LEFT:
            return True
        if self._head_on_lower_boarder(current_head_pos) and next_step == NextStep.DOWN:
            return True

        if (
            self._head_on_right_boarder(current_head_pos)
            and next_step == NextStep.RIGHT
        ):
            return True
        if self._head_on_upper_boarder(current_head_pos) and next_step == NextStep.UP:
            return True
        return False

    def _head_on_left_boarder(self, current_head_pos):
        return current_head_pos[0] == 0

    def _head_on_lower_boarder(self, current_head_pos):
        return current_head_pos[1] == 0

    def _head_on_right_boarder(self, current_head_pos):
        return current_head_pos[0] == self.board_width - 1

    def _head_on_upper_boarder(self, current_head_pos):
        return current_head_pos[1] == self.board_height - 1
