from collections import deque
from dataclasses import dataclass
from enum import Enum
from itertools import islice
from typing import Iterable, Optional, Protocol


class NextStep(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True, slots=True)
class Position:
    x: int
    y: int


class Snake:
    """Representation of one single snake.

    If the snake is myself it's marked with is_me flag.
    """

    def __init__(self, head_and_body: list[Position], is_me=False):
        self._head_and_body: deque[Position] = deque(head_and_body)
        self.is_me: bool = is_me
        self.id = self._head_and_body[0]

    @classmethod
    def from_dict(cls, **snake_data: dict) -> "Snake":
        head_and_body: list[Position] = [
            Position(**position) for position in snake_data["body"]
        ]
        return cls(head_and_body)

    @property
    def head_and_body(self) -> list[Position]:
        return list(self._head_and_body)

    @property
    def head(self) -> Position:
        return self._head_and_body[0]

    @property
    def body_without_head(self) -> list[Position]:
        return list(islice(self._head_and_body, 1, None))

    def __len__(self):
        return len(self._head_and_body)

    def __str__(self):
        return SnakeVisualizer(self).snake_in_11x11_board

    def calculate_future_snake(
        self,
        next_step: NextStep,
        is_food_available: bool = False,
    ) -> "FutureSnake":
        """Return a new theoretical posibble snake based on the next step and available food."""

        return FutureSnake(self, next_step, is_food_available)

    def bites_itself(self) -> bool:
        return self.head in self.body_without_head


class FutureSnake(Snake):
    """Create a theoretical new snake based on the next step and available food.

    The resulting snake is just theoretical, because it will be created even if
    it does bite itself or if it would fall out of the gaming board.
    Food leads to the growth of the snake: The head will move forward but the rest
    of the body stays.

    Special case for very small snakes at the beginning of the game:
    Until the snake is smaller than 3 (inc. head) it will grow, even if there's no
    food available.

    The future snake remembers its 'mother' as well as the first "next_step"
    that created this snake and further successors in the first place.
    A FutureSnake can calculate another FutureSnake. Every FutureSnake can
    go back to the very first next_step of the earliest ancestor.

    Args:
        next_step (NextStep): Direction for the next step.
        is_food_available (bool, optional): Is there currenlty food beneath the
            snake's head? Defaults to False.

    Returns:
        FutureSnake: Brand new 'theoretical' snake how it would look like in the future after the next step."""

    def __init__(
        self,
        mother,
        next_step: NextStep,
        is_food_available: bool,
    ):
        self.mother: Snake | FutureSnake = mother
        self._head_and_body = mother._head_and_body.copy()
        self.step_made_to_get_here = next_step
        if type(mother) == Snake:
            self.my_first_step = next_step
        elif type(mother) == FutureSnake:
            self.my_first_step = mother.my_first_step  # type: ignore
        self.is_me = mother.is_me
        self._is_food_available_at_creation_time = is_food_available
        self._calculate_future_body()
        # One ID is the same for all possible-future-snakes that is based on one "normal" Snake
        self.id = mother.id

    def _calculate_future_body(self):
        self._add_future_head_to_future_snake()
        if self._is_still_baby_snake():
            self._is_food_available_at_creation_time = True
        if not self._is_food_available_at_creation_time:
            self._remove_tail()

    def _add_future_head_to_future_snake(self):
        future_head_position: Position = self._calc_future_head_position()
        self._head_and_body.appendleft(future_head_position)

    def _calc_future_head_position(self) -> Position:
        if self.step_made_to_get_here == NextStep.UP:
            return Position(self.head.x, self.head.y + 1)
        if self.step_made_to_get_here == NextStep.DOWN:
            return Position(self.head.x, self.head.y - 1)
        if self.step_made_to_get_here == NextStep.RIGHT:
            return Position(self.head.x + 1, self.head.y)
        if self.step_made_to_get_here == NextStep.LEFT:
            return Position(self.head.x - 1, self.head.y)
        else:
            raise ValueError(f"Next step not defined: {self.step_made_to_get_here}")

    def _is_still_baby_snake(self):
        return len(self.mother) < 3

    def _remove_tail(self):
        self._head_and_body.pop()

    def get_my_first_step(self) -> NextStep:
        """Get the first step from the first FutureSnake in this line of relatives"""
        return self.my_first_step

    def __repr__(self) -> str:
        return f"FutureSnake: ID={self.id}, HEAD={self.head}, MOTHER={self.mother.head}"


class SnakeVisualizer:
    """Visualize snake in 11 x 11 field"""

    def __init__(self, snake: Snake):
        self._snake = snake
        self._visual_board: list[list[str]] = self._init_11x11_board()
        self._visualize()
        self.snake_in_11x11_board: str

    def _visualize(self):
        for pos in self._snake.head_and_body:
            self._enter_snake_into_visual_board(pos)
        self._paint_field_walls()
        self._convert_board_array_to_str()

    def _init_11x11_board(self) -> list[list[str]]:
        field: list[list[str]] = [["·" for _ in range(11)] for _ in range(11)]
        return field

    def _enter_snake_into_visual_board(self, pos: Position):
        char_for_body_limb = "x"
        if pos == self._snake.head:
            char_for_body_limb = "o"
        self._visual_board[10 - pos.y][pos.x] = char_for_body_limb

    def _paint_field_walls(self):
        self._visual_board.insert(0, ["=" for _ in range(11)])
        self._visual_board.append(["=" for _ in range(11)])
        for row in self._visual_board:
            row.insert(0, "|")
            row.append("|")

    def _convert_board_array_to_str(self):
        convert_row = lambda row: "".join([cell for cell in row])
        self.snake_in_11x11_board = "\n".join(
            convert_row(row) for row in self._visual_board
        )


class Board:
    """Represents the board including board size, all snakes, food and position of my own snake."""

    def __init__(
        self,
        bounderies: "GameBoardBounderies",
        food: set[Position],
        snakes: set[Snake],
    ):
        self.bounderies: "GameBoardBounderies" = bounderies
        self.food: set[Position] = food
        self.snakes: set[Snake] = snakes
        self._my_snake: Snake = [snake for snake in self.snakes if snake.is_me][0]

    @classmethod
    def from_dict(cls, game_request: dict) -> "Board":
        board_data: dict = game_request["board"]
        my_head_pos = Position(**game_request["you"]["head"])
        bounderies = GameBoardBounderies(board_data["height"], board_data["width"])
        food = {Position(**position_data) for position_data in board_data["food"]}
        snakes = {Snake.from_dict(**snake_data) for snake_data in board_data["snakes"]}
        my_snake = [snake for snake in snakes if snake.head == my_head_pos].pop()
        my_snake.is_me = True
        return cls(bounderies, food, snakes)

    @property
    def my_snake(self) -> Snake:
        return self._my_snake


class GameBoardBounderies:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def is_wall(self, pos: Position) -> bool:
        if pos.x < 0 or pos.y < 0:
            return True
        if pos.x >= self.width:
            return True
        if pos.y >= self.height:
            return True
        return False

    def __eq__(self, other: "GameBoardBounderies") -> bool:
        return self.height == other.height and self.width == other.width


class Recorder(Protocol):
    """Record history of all information of interest of the PossibleFutureBoard"""

    def save(self, board: "PossibleFutureBoard"):
        ...


class PossibleFutureBoard:
    """Simulate Board as it could look like in the future.

    Add all possible future snakes for every new step.
    Remove only snakes biting itself or running into walls.

    For the first step only (deterministic regarding the body):
    Remove in addition snakes, biting other snakes for sure
    (during initializing the PossibleFutureBoard).

    Remove eaten food after calculating the next_turn.

    Several turns can be simulated using next_turn.
    For performance reasons it's possible to register a recorder
    to evaluate interesting information later on.
    """

    def __init__(self, board: Board):
        self.bounderies: GameBoardBounderies = board.bounderies
        self.food: set[Position] = board.food.copy()
        self.possible_snakes: set[FutureSnake] = set()
        self.recorder: Optional[Recorder] = None
        self._prepare_future_board(board.snakes)
        # only deterministic in first step
        self._remove_snakes_biting_other_snakes()
        self.simulated_turns: int = 1

    def _prepare_future_board(self, orig_snakes: Iterable[Snake]):
        self.possible_snakes = set()
        self._add_possible_snakes_of_future(orig_snakes)

    def _add_possible_snakes_of_future(self, orig_snakes: Iterable[Snake]):
        for original_snake in orig_snakes:
            self._add_possible_variants_of_one_snake_to_future_board(original_snake)

    def _add_possible_variants_of_one_snake_to_future_board(
        self, original_snake: Snake | FutureSnake
    ):
        for step in NextStep:
            future_snake = self._make_future_snake(original_snake, step)
            if future_snake.bites_itself() or self.is_wall(future_snake.head):
                continue
            self.possible_snakes.add(future_snake)

    def _make_future_snake(
        self, snake: Snake | FutureSnake, step: NextStep
    ) -> FutureSnake:
        has_food = self.is_food_available_for(snake)
        return snake.calculate_future_snake(step, has_food)

    def is_food_available_for(self, snake: Snake):
        return snake.head in self.food

    def _remove_snakes_biting_other_snakes(self):
        snake_bodies = [
            position
            for snake in self.possible_snakes
            for position in snake.body_without_head
        ]

        for snake in self.possible_snakes.copy():
            if snake.head in snake_bodies:
                self.possible_snakes.remove(snake)

    def _remove_eaten_food(self, orig_snakes: Iterable[Snake]):
        for snake in orig_snakes:
            self._remove_food_eaten_by(snake)

    def _remove_food_eaten_by(self, snake: Snake):
        if self.is_food_available_for(snake):
            self.food.remove(snake.head)

    def is_wall(self, pos: Position) -> bool:
        return self.bounderies.is_wall(pos)

    def get_my_survived_snakes(self) -> set[FutureSnake]:
        return {snake for snake in self.possible_snakes if snake.is_me}

    def next_turn(self) -> None:
        orig_snakes = self.possible_snakes.copy()
        self._remove_eaten_food(orig_snakes)
        self._prepare_future_board(orig_snakes)
        self.simulated_turns += 1
        if self.recorder:
            self.recorder.save(self)

    def register_recorder(self, recorder: Recorder):
        self.recorder = recorder
        self.recorder.save(self)

    def does_my_snake_bite_or_collide_with_another_snake(
        self, my_snake: FutureSnake
    ) -> bool:
        assert my_snake.is_me
        for other_snake in self.possible_snakes:
            if other_snake.is_me:
                continue
            if my_snake.head in other_snake.body_without_head:
                return True
            if self._is_possible_dangerous_head_collision(my_snake, other_snake):
                return True
        return False

    def _is_possible_dangerous_head_collision(
        self, my_snake: FutureSnake, other_snake: FutureSnake
    ) -> bool:
        return my_snake.head == other_snake.head and len(my_snake) <= len(other_snake)
