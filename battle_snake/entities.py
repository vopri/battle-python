import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional
from xmlrpc.client import Boolean


class NextStep(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True, slots=True)
class Position:
    x: int
    y: int


class BattleSnakeException(Exception):
    ...


class Snake:
    """Representation of one single snake.

    If the snake is myself it's marked with is_me = True
    """

    def __init__(self, head_and_body: list[Position], is_me=False):
        self.head_and_body: list[Position] = head_and_body
        self.is_me: bool = is_me
        self.id = self.head_and_body[0]

    @classmethod
    def from_dict(cls, **snake_data: dict) -> "Snake":
        head_and_body: list[Position] = [
            Position(**position) for position in snake_data["body"]
        ]
        return cls(head_and_body)

    @property
    def head(self) -> Position:
        return self.head_and_body[0]

    @property
    def body_without_head(self) -> list[Position]:
        return self.head_and_body[1:]

    @property
    def neck(self) -> Position:
        return self.head_and_body[1]

    def __len__(self):
        return len(self.head_and_body)

    def __str__(self):
        return SnakeVisualizer(self).snake_in_11x11_board

    def calculate_future_snake(
        self,
        next_step: NextStep,
        is_food_available: bool = False,
    ) -> "FutureSnake":
        """Return a new theoretical posibble snake based on the next step and available food."""

        return FutureSnake(self, next_step, is_food_available)

    def bites_itself(self) -> Boolean:
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

    The future snake remembers its 'mother' as well as the mother's next_step
    that created this snake in the first place.
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
        self.head_and_body = mother.head_and_body.copy()
        self.step_made_to_get_here = next_step
        if type(mother) == Snake:
            self.my_first_step = next_step
        elif type(mother) == FutureSnake:
            self.my_first_step = mother.my_first_step  # type: ignore
        self.is_me = mother.is_me
        self._is_food_available_at_beginning = is_food_available
        self._calculate_future_body()
        # One ID is the same for all possible-future-snakes that is based on one "normal" Snake
        self.id = mother.id

    def _calculate_future_body(self):
        self._add_future_head_to_future_snake()
        if self._is_still_baby_snake():
            self._is_food_available_at_beginning = True
        if not self._is_food_available_at_beginning:
            self._remove_tail()

    def _add_future_head_to_future_snake(self):
        future_head_position: Position = self._calc_future_head_position()
        self.head_and_body.insert(0, future_head_position)

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
        self.head_and_body.pop()

    def get_my_first_step(self) -> NextStep:
        """Get the first step from the first FutureSnake in this line of relatives"""
        return self.my_first_step

    def find_first_future_snake_of_my_ancestors(self):
        snake: FutureSnake = self
        while True:
            if type(snake.mother) == Snake:
                break
            elif type(snake.mother) == self.__class__:
                snake = snake.mother  # type: ignore
            else:
                raise BattleSnakeException()
        return snake

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
        return [snake for snake in self.snakes if snake.is_me][0]


class FutureBoard:
    """Calculate how the board could look like in the next turn.

    Deterministic is the body of all snakes.
    Unclear is the position of their heads.

    This method will include all possible snakes, including "mine".
    "Impossible snakes" will be removed.

    Impossible means:
    - running into walls
    - disqualified by eating itself or others
    - only after using next_turn: dying snake due to *certain* head  collision with snake of same size or bigger.
    Snakes with *possible* but not completely certain head collisions will stay on the board.
    The head collision risk can be calculated per FutureSnake dynamically.

    All possible head positions are included (pessimistic approach).
    All "eaten" food from the current turn will be removed.

    The FutureBoard doesn't derive from Board because of Liskov Substitution Principle:
    not fitting: all_snakes vs. all_possible_snakes etc.

    """

    def __init__(self, board: Board):
        self.bounderies: GameBoardBounderies = board.bounderies
        self.food: set[Position] = {food for food in board.food}
        self.all_possible_snakes: set[FutureSnake] = set()
        self._positions_of_all_snakes_bodies: set[Position] = set()
        self._prepare_future_board(board.snakes)
        self.simulated_turns: int = 1

    def _prepare_future_board(self, orig_snakes: Iterable[Snake]):
        self.all_possible_snakes.clear()
        self._add_all_possible_snakes_of_future(orig_snakes)
        self._positions_of_all_snakes_bodies = self._calc_all_body_fields()
        self._remove_snakes_running_into_walls()
        self._remove_snakes_disqualified_due_to_biting()
        self._remove_eaten_food(orig_snakes)

    def _add_all_possible_snakes_of_future(self, orig_snakes: Iterable[Snake]):
        """Add all possible snakes (including mine) to the board.

        - All snakes that do not bite itself.
        - There are up to 3 snake-copies in the future board for every
        original snake, 1 for every direction (as long as it doesn't bite itself)
        """
        for original_snake in orig_snakes:
            self._add_all_possible_variants_of_one_snake_to_future_board(original_snake)

    def _add_all_possible_variants_of_one_snake_to_future_board(self, original_snake):
        for next_possible_step in self._get_all_possible_steps():
            future_snake = self._make_future_snake(original_snake, next_possible_step)
            self.all_possible_snakes.add(future_snake)

    def _get_all_possible_steps(self):
        return (
            NextStep.UP,
            NextStep.DOWN,
            NextStep.RIGHT,
            NextStep.LEFT,
        )

    def _make_future_snake(self, snake, next_possible_step):
        future_snake = snake.calculate_future_snake(
            next_possible_step, self.is_food_available_for(snake)
        )
        return future_snake

    def is_food_available_for(self, snake: Snake):
        return snake.head in self.food

    def _remove_snakes_running_into_walls(self):
        self.all_possible_snakes = {
            snake for snake in self.all_possible_snakes if not self.is_wall(snake.head)
        }

    def _remove_snakes_disqualified_due_to_biting(self):
        """All snakes that are *defenitely* diqualified, because biting another snake or itself are removed.

        What means 'definitely'? Based on current position and food the body
        of every snake in the future step is deterministic. But the snake's heads
        are not deterministic. They depend from individual decisions of the snakes.
        Therefore the method will *not* remove snakes that might be disqualified due to
        head collisions, but only snake that are disqualified because they bite
        into another body (excl. head).
        """

        self.all_possible_snakes = {
            snake
            for snake in self.all_possible_snakes
            if not self._is_disqualified_due_to_biting(snake)
        }

    def _is_disqualified_due_to_biting(self, snake) -> bool:
        return snake.head in self._get_all_body_fields()

    def _calc_all_body_fields(self) -> set[Position]:
        return {
            pos for snake in self.all_possible_snakes for pos in snake.body_without_head
        }

    def _get_all_body_fields(self) -> set[Position]:
        return self._positions_of_all_snakes_bodies

    def calc_head_collision_risk_for(self, future_snake: FutureSnake) -> float:
        """Calculate probability of dangerous head collision for one future snake

        We are coping with probability for non-mutually exclusive events!
        Calculation of the probability of snake head collisions is done using the addition rule.
        The probability of several non-mutually exclusive events (like in this case) can be calculated
        using the rules of De Morgan.

        P(S1 ∪ S2 ∪ S3) = 1 - (1-P(S1) * 1-P(S2) * 1-P(S3)).

        P(S1) is calculated as 1/(amount of variants, i.e. possible moves, of snake S1)

        Example 1: There are 2 snakes (A & B) that could collide with the investigated snake here
        * Snake A: collides with P(1/2)=50% (1 out of 2 possible moves)
        * Snake B: collides with P(1/3)=33% (1 out of 3 possible moves)
        * Calculation: 1 - (1/2 * 2/3) = 2/3 = 66%

        * Example 2:
        * Snake A: collides with probability of 100% (1 / 1 possible moves)
        * Snake B: collides with probability of 1/3 = 33% (1 / 3 possible moves)
        * Calculatoin: 1 - (0 * 2/3) = 1 = 100%
        """
        dangerous_snakes = self._get_future_dangerous_snakes(future_snake)
        if not dangerous_snakes:
            return 0
        amount_of_moves_of_dangerour_snakes = (
            self._get_possible_moves_of_dangerous_snakes(dangerous_snakes)
        )
        inverse_risks_of_dangrous_snake_head_collisions = [
            1 - (1 / amount_of_moves)
            for amount_of_moves in amount_of_moves_of_dangerour_snakes
        ]
        total_risk = 1 - math.prod(inverse_risks_of_dangrous_snake_head_collisions)
        return total_risk

    def _get_future_dangerous_snakes(
        self, future_snake: FutureSnake
    ) -> Iterable[FutureSnake]:
        """Get future snakes that are dangerous in sense of head collision.

        Args:
            future_snake (FutureSnake): FutureSnake that head collision risk is calculated for
        """
        return {
            some_snake
            for some_snake in self.all_possible_snakes
            if self._will_heads_collide(some_snake, future_snake)
            and self._is_lenght_of_some_snake_dangerous_for_future_snake(
                some_snake, future_snake
            )
            and self._is_really_another_snake_and_not_just_a_variant_of_myself(
                some_snake, future_snake
            )
        }

    def _will_heads_collide(self, some_snake: FutureSnake, other_snake: FutureSnake):
        return some_snake.head == other_snake.head

    def _is_lenght_of_some_snake_dangerous_for_future_snake(
        self, some_snake, future_snake: FutureSnake
    ):
        return len(some_snake) >= len(future_snake)

    def _is_really_another_snake_and_not_just_a_variant_of_myself(
        self, some_snake: FutureSnake, future_snake: FutureSnake
    ):
        return some_snake.id != future_snake.id

    def _get_possible_moves_of_dangerous_snakes(
        self, dangerous_snakes
    ) -> Iterable[int]:
        return {
            self._count_dangerous_snake_and_siblings(dangrous_snake)
            for dangrous_snake in dangerous_snakes
        }

    def _count_dangerous_snake_and_siblings(self, dangrous_snake) -> int:
        snakes = {
            snake
            for snake in self.all_possible_snakes
            if snake.id == dangrous_snake.id
            and snake.mother.head == dangrous_snake.mother.head
        }
        return len(snakes)

    def _remove_eaten_food(self, orig_snakes: Iterable[Snake]):
        for snake in orig_snakes:
            self._remove_food_eaten_by(snake)

    def _remove_food_eaten_by(self, snake: Snake):
        if self.is_food_available_for(snake):
            self.food.remove(snake.head)

    def is_wall(self, pos: Position) -> bool:
        """Check for dangerous wall on given position.

        Args:
            pos (Position): Coordinates on the board.

        Returns:
            bool: Is there a wall?
        """
        return self.bounderies.is_wall(pos)

    def get_my_survived_snakes(self) -> set[FutureSnake]:
        return {snake for snake in self.all_possible_snakes if snake.is_me}

    def _remove_snakes_which_will_die_by_head_collision(self):
        for snake in self.all_possible_snakes.copy():
            if self.calc_head_collision_risk_for(snake) == 1:
                self.all_possible_snakes.remove(snake)

    def next_turn(self) -> None:
        # Removal of head-collision snakes during next_turn only
        # (instead of during init of Board),
        # because otherwise the removal would have unwanted side effects
        # on calculation of head collision risk
        # self._remove_snakes_which_will_die_by_head_collision()
        orig_snakes = self.all_possible_snakes.copy()
        self._prepare_future_board(orig_snakes)
        self.simulated_turns += 1


class GameBoardBounderies:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

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

    def __eq__(self, other: "GameBoardBounderies") -> bool:
        return self.height == other.height and self.width == other.width


class PossibleFutureBoard:
    def __init__(self, board: Board):
        self.bounderies: GameBoardBounderies = board.bounderies
        self.food: set[Position] = {food for food in board.food}
        self.all_possible_snakes: set[FutureSnake] = set()
        self._prepare_future_board(board.snakes)
        self.simulated_turns: int = 1

    def _prepare_future_board(self, orig_snakes: Iterable[Snake]):
        self.all_possible_snakes.clear()
        self._add_all_possible_snakes_of_future(orig_snakes)
        self._remove_snakes_running_into_walls()
        self._remove_snakes_biting_itself()

    def _add_all_possible_snakes_of_future(self, orig_snakes: Iterable[Snake]):
        for original_snake in orig_snakes:
            self._add_all_possible_variants_of_one_snake_to_future_board(original_snake)

    def _add_all_possible_variants_of_one_snake_to_future_board(self, original_snake):
        for next_possible_step in self._get_all_possible_steps():
            future_snake = self._make_future_snake(original_snake, next_possible_step)
            self.all_possible_snakes.add(future_snake)

    def _get_all_possible_steps(self):
        return (
            NextStep.UP,
            NextStep.DOWN,
            NextStep.RIGHT,
            NextStep.LEFT,
        )

    def _make_future_snake(self, snake, next_possible_step):
        future_snake = snake.calculate_future_snake(
            next_possible_step, self.is_food_available_for(snake)
        )
        return future_snake

    def is_food_available_for(self, snake: Snake):
        return snake.head in self.food

    def _remove_snakes_running_into_walls(self):
        self.all_possible_snakes = {
            snake for snake in self.all_possible_snakes if not self.is_wall(snake.head)
        }

    def _remove_snakes_biting_itself(self):
        self.all_possible_snakes = {
            snake for snake in self.all_possible_snakes if not snake.bites_itself()
        }

    def _remove_eaten_food(self, orig_snakes: Iterable[Snake]):
        for snake in orig_snakes:
            self._remove_food_eaten_by(snake)

    def _remove_food_eaten_by(self, snake: Snake):
        if self.is_food_available_for(snake):
            self.food.remove(snake.head)

    def is_wall(self, pos: Position) -> bool:
        """Check for dangerous wall on given position.

        Args:
            pos (Position): Coordinates on the board.

        Returns:
            bool: Is there a wall?
        """
        return self.bounderies.is_wall(pos)

    def get_my_survived_snakes(self) -> set[FutureSnake]:
        return {snake for snake in self.all_possible_snakes if snake.is_me}

    def next_turn(self) -> None:
        orig_snakes = self.all_possible_snakes.copy()
        self._remove_eaten_food(orig_snakes)
        self._prepare_future_board(orig_snakes)
        self.simulated_turns += 1
