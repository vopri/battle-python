from dataclasses import dataclass
from enum import Enum


class NextStep(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int


Moves = dict[Position, NextStep]  # type alias


class Snake:
    """Representation of one single snake.

    If the snake is myself it's marked with is_me = True
    """

    def __init__(self, **snake_data: dict):
        self.body_and_head: list[Position] = [
            Position(**position) for position in snake_data["body"]
        ]
        self.is_me: bool = False

    @property
    def head(self) -> Position:
        return self.body_and_head[0]

    @property
    def body_without_head(self) -> list[Position]:
        return self.body_and_head[1:]

    @property
    def neck(self) -> Position:
        return self.body_and_head[1]

    @property
    def tail(self) -> Position:
        return self.body_and_head[-1]

    def __len__(self):
        return len(self.body_and_head)

    def __str__(self):
        return SnakeVisualizer(self).snake_in_11x11_board

    def get_next_theoretical_moves(self) -> Moves:
        """Give all 4 theoretically possible coordinates of snake's head for the next move.

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
        is_food_available: bool = False,
    ) -> "FutureSnake":
        """Return a new theoretical posibble snake based on the next step and available food."""

        return FutureSnake(self, next_step, is_food_available)


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

    def __init__(self, mother: Snake, next_step: NextStep, is_food_available: bool):
        self.mother = mother
        self.body_and_head = mother.body_and_head[:]
        self.step_made_to_get_here = next_step
        self.is_me = mother.is_me
        self.is_food_available = is_food_available
        self._calculate_future_body()

    def _calculate_future_body(self):
        self._add_future_head_to_future_snake()
        if self._is_still_baby_snake():
            self.is_food_available = True
        if not self.is_food_available:
            self._remove_tail()

    def _add_future_head_to_future_snake(self):
        future_head_position: Position = self._calc_future_head_position()
        self.body_and_head.insert(0, future_head_position)

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
        self.body_and_head.pop()

    def does_bite_itself(self) -> bool:
        return self.head in self.body_without_head

    def get_my_first_step(self) -> NextStep:
        """Get the first step from the first FutureSnake in this line of relatives"""

        first_future_snake = self._find_first_future_snake_of_my_ancestors()
        return first_future_snake.step_made_to_get_here

    def _find_first_future_snake_of_my_ancestors(self):
        snake: FutureSnake = self
        while True:
            if type(snake.mother) == Snake:
                break
        return snake


class SnakeVisualizer:
    """Visualize snake in 11 x 11 field"""

    def __init__(self, snake: Snake):
        self._snake = snake
        self._visual_board: list[list[str]] = self._init_11x11_board()
        self._visualize()
        self.snake_in_11x11_board: str

    def _visualize(self):
        for pos in self._snake.body_and_head:
            self._enter_snake_into_visual_board(pos)
        self._paint_field_walls()
        self._convert_board_array_to_str()

    def _init_11x11_board(self) -> list[list[str]]:
        field: list[list[str]] = [["·" for i in range(11)] for j in range(11)]
        return field

    def _enter_snake_into_visual_board(self, pos: Position):
        char_for_body_limb = "x"
        if pos == self._snake.head:
            char_for_body_limb = "o"
        self._visual_board[10 - pos.y][pos.x] = char_for_body_limb

    def _paint_field_walls(self):
        self._visual_board.insert(0, ["=" for i in range(11)])
        self._visual_board.append(["=" for i in range(11)])
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

    def __init__(self, my_head: Position, **board_data: dict):
        self._board_data: dict = board_data
        self._bounderies: GameBoardBounderies = self._find_board_bounderies()
        self.food: set[Position] = self._find_food()
        self.all_snakes: dict[Position, Snake] = self._find_snakes()
        self._my_head: Position = my_head
        self._let_my_snake_know_who_it_is()

    def _find_board_bounderies(self):
        return GameBoardBounderies(
            self._board_data["height"], self._board_data["width"]
        )

    def _find_food(self):
        return {Position(**position_data) for position_data in self._board_data["food"]}

    def _find_snakes(self):
        return {
            Position(**snake_data["head"]): Snake(**snake_data)
            for snake_data in self._board_data["snakes"]
        }

    def _let_my_snake_know_who_it_is(self):
        self.my_snake.is_me = True

    @property
    def my_snake(self) -> Snake:
        return self.all_snakes[self._my_head]

    def is_wall(self, pos: Position) -> bool:
        """Check for wall on given position."""
        return self._bounderies.is_wall(pos)


class FutureBoard:
    """Calculate how the board could look like in the next turn.

    Deterministic is the body of all snakes.
    Unclear is the position of their heads.

    This method will include all possible snakes, including mine.
    "Impossible snakes" will be removed.

    Impossible means:
    - running into walls
    - disqualified by eating itself or others
    - dependending from risk_tolerance:
        - if 0: not risk tolerant at all -> avoid all possible head collisions with snakes in same size or bigger
        - if 1: very risk tolerant -> don't care if you would collided with another snake's head

    All possible head positions are included (pessimistic approach).
    All "eaten" food from the current turn will be removed.

    The FutureBoard doesn't derive from Board because of Liskov Substitution Principle:
    not fitting: all_snakes vs. all_possible_snakes etc.
    To avoid DRY GameBoardBounderies is extracted.

    """

    def __init__(self, board: Board, risk_tolerance: float = 0):
        self._orig_board = board
        self._bounderies: GameBoardBounderies = board._bounderies
        self.food: set[Position] = {food for food in board.food}
        self.all_possible_snakes: list[FutureSnake] = []
        self.risk_tolerance: float = risk_tolerance
        self._add_all_possible_snakes_of_future()
        self._remove_snakes_running_into_walls()
        self._remove_snakes_disqualified_due_to_biting()
        self._remove_my_snakes_with_possible_head_collision()
        self._remove_eaten_food()

    def _add_all_possible_snakes_of_future(self):
        """Add all possible snakes (including mine) to the board.

        - All snakes that do not bite itself.
        - There are up to 3 snake-copies in the future board for every
        original snake, 1 for every direction (as long as it doesn't bite itself)
        """
        snakes_of_mother_board = self._orig_board.all_snakes.values()
        for original_snake in snakes_of_mother_board:
            self._add_all_possible_variants_of_one_snake_to_future_board(original_snake)

    def _add_all_possible_variants_of_one_snake_to_future_board(self, original_snake):
        for next_possible_step in self._get_all_possible_steps():
            future_snake = self._make_future_snake(original_snake, next_possible_step)
            self.all_possible_snakes.append(future_snake)

    def _get_all_possible_steps(self):
        return (
            NextStep.UP,
            NextStep.DOWN,
            NextStep.RIGHT,
            NextStep.LEFT,
        )

    def _make_future_snake(self, snake, next_possible_step):
        future_snake = snake.calculate_future_snake(
            next_possible_step, self._is_food_available_for(snake)
        )
        return future_snake

    def _is_food_available_for(self, snake: Snake):
        return snake.head in self.food

    def _remove_snakes_running_into_walls(self):
        self.all_possible_snakes = [
            snake for snake in self.all_possible_snakes if not self.is_wall(snake.head)
        ]

    def _remove_snakes_disqualified_due_to_biting(self):
        """All snakes that are *defenitely* diqualified, because biting another snake or itself are removed.

        What means 'definitely'? Based on current position and food the body
        of every snake in the future step is deterministic. But the snake's heads
        are not deterministic. They depend from individual decisions of the snakes.
        Therefore the method will *not* remove snakes that might be disqualified due to
        head collisions, but only snake that are disqualified because they bite
        into another body (excl. head).
        """

        self.all_possible_snakes = [
            snake
            for snake in self.all_possible_snakes
            if not self._is_disqualified_due_to_biting(snake)
        ]

    def _is_disqualified_due_to_biting(self, snake) -> bool:
        return snake.head in self._get_all_body_fields()

    def _get_all_body_fields(self) -> set[Position]:
        return {
            pos for snake in self.all_possible_snakes for pos in snake.body_without_head
        }

    def _remove_my_snakes_with_possible_head_collision(self):
        i_dont_care_about_head_collisions = self.risk_tolerance == 1
        if i_dont_care_about_head_collisions:
            return
        my_risky_snake_variants = {
            snake
            for snake in self.all_possible_snakes
            if snake.is_me
            and self.risk_tolerance < self.calc_snake_head_risk_value(snake.head)
        }
        for my_risky_snake in my_risky_snake_variants:
            self.all_possible_snakes.remove(my_risky_snake)

    def _remove_eaten_food(self):
        for snake in self._orig_board.all_snakes.values():
            self._remove_food_eaten_by(snake)

    def _remove_food_eaten_by(self, snake: Snake):
        if self._is_food_available_for(snake):
            self.food.remove(snake.head)

    # TODO: Remove after changing the interactor later on
    def is_other_snake_body_on_this(self, position: Position) -> bool:
        if self._is_no_snake_body_on_this(position):
            return False
        if self._is_one_of_my_own_future_bodies_on_this(position):
            return False
        return True

    # TODO: Remove after changing the interactor later on
    def _is_no_snake_body_on_this(self, position):
        return not position in self._get_all_body_fields()

    # TODO: Remove after changing the interactor later on
    def _is_one_of_my_own_future_bodies_on_this(self, position):
        return position in [
            position
            for snake in self.all_possible_snakes
            for position in snake.body_without_head
            if snake.is_me
        ]

    def calc_snake_head_risk_value(self, pos: Position) -> float:
        """Calculate a risk between 0 and 1 that there's a dangerous snake head.

        Dangerous means that the snake is at least of my lenght.
        Args:
            pos (Position): Position to check for

        Returns:
            float: Risk value as sum of probability of all snakes with their head on this position.
        """
        probabilities_of_snakes_on_pos = [
            (1 / self._count_snakes_by_neck_position(neck_pos))
            for neck_pos in self._get_danger_snake_neck_id_with_head_on_pos(pos)
        ]
        risk_value = sum(probabilities_of_snakes_on_pos)
        return risk_value

    def _count_snakes_by_neck_position(self, pos: Position) -> int:
        snake_variants = [
            snake for snake in self.all_possible_snakes if snake.neck == pos
        ]
        return len(snake_variants)

    def _get_danger_snake_neck_id_with_head_on_pos(
        self, head_pos: Position
    ) -> list[Position]:
        """Return a list with neck positions of all snakes here, that can be dangerous for me.

        Dangerous means, they are longer or equals long as me.
        Args:
            position (Position): Position to check for dangouers snakes.

        Returns:
            list[Position]: List of neck positions, because the neck is on the same position
            for all possible variants of 1 snake in the future board of possiblities.
            The neck of 1 snake in all possible variants can only be on one position.
            And on one position there can only be one neck.
        """
        dangerous_size = len(self._orig_board.my_snake)
        return [
            snake.neck
            for snake in self.all_possible_snakes
            if snake.head == head_pos
            and len(snake) >= dangerous_size
            and not snake.is_me
        ]

    def is_wall(self, pos: Position) -> bool:
        """Check for dangerous wall on given position.

        Args:
            pos (Position): Coordinates on the board.

        Returns:
            bool: Is there a wall?
        """
        return self._bounderies.is_wall(pos)

    def get_my_survived_snakes(self) -> set[FutureSnake]:
        return {snake for snake in self.all_possible_snakes if snake.is_me}

    def get_first_steps_of_my_survived_snakes(self) -> set[NextStep]:
        return {snake.get_my_first_step() for snake in self.get_my_survived_snakes()}


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
