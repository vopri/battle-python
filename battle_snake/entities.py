import copy
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
    """Representation of one single snake."""

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
        field: list[list[str]] = self._init_field()
        for pos in self.body_incl_head:
            self._enter_snake_into_field(field, pos)
        self._paint_field_walls(field)
        convert_row = lambda row: "".join([cell for cell in row])
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
        """Give all possible 4 theoretically possible coordinates of snake's head for the next move.

        The returned positions are just theoretically possible and do not take care
        of hitting walls, my own body or other snakes. Therefore the position can
        even have negative coordinates.

        Returns:
            dict[Position, NextStep]: Dictionary with 4 entries where:
            key represents the coordinates on the field
            value represents the direction for the next move that leads to that position
        """
        result = dict()
        result[Position(self.head.x + 1, self.head.y)] = NextStep.RIGHT
        result[Position(self.head.x - 1, self.head.y)] = NextStep.LEFT
        result[Position(self.head.x, self.head.y + 1)] = NextStep.UP
        result[Position(self.head.x, self.head.y - 1)] = NextStep.DOWN
        return result

    def calculate_future_snake(
        self,
        next_step: NextStep,
        food: bool = False,
    ) -> "Snake":
        """Return a new snake based on the next step into one defined direction.

        The resulting snake is a deepcopy without any references to the original snake.
        It is taken into consideration if there's food beneath the snakes head.
        Food leads to the growth of the snake: The head will move forward but the rest
        of the body stays. Without food (and therefore without any growth) the snake's
        body will change its position entirely.

        Args:
            next_step (NextStep): Direction for the next step.
            food (bool, optional): Is there currenlty food beneath the snakes head? Defaults to False.

        Returns:
            Snake: Brand new snake how it would look like in the future after the next step.
        """
        future_snake: Snake = copy.deepcopy(self)
        future_head_position: Position = self._calc_future_head_position(next_step)
        self._add_future_head_to_future_snake(future_snake, future_head_position)
        if not food:
            self._remove_tail(future_snake)
        return future_snake

    def _calc_future_head_position(self, next_step):
        return [
            position
            for position, n_step in self.next_theoretical_head_positions_and_moves().items()
            if n_step == next_step
        ][0]

    def _add_future_head_to_future_snake(self, future_snake, future_head_position):
        future_snake.body_incl_head.insert(0, future_head_position)

    def _remove_tail(self, future_snake):
        future_snake.body_incl_head.pop()


class Board:
    """Represents the board including board size, all snakes, food and position of my own snake."""

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
        """Check for dangerous wall on given position.

        Args:
            pos (Position): Coordinates on the board.

        Returns:
            bool: Is there a wall?
        """
        if pos.x < 0 or pos.y < 0:
            return True
        if pos.x >= self.width:
            return True
        if pos.y >= self.height:
            return True
        return False
