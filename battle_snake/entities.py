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
    ) -> "Snake":
        """Return a new snake based on the next step into one defined direction.

        The resulting snake is a deepcopy without any references to the original snake.
        It is taken into consideration if there's food beneath the snakes head.
        Food leads to the growth of the snake: The head will move forward but the rest
        of the body stays. Without food (and therefore without any growth) the snake's
        body will change its position entirely.

        Special case for very small cases at the beginning of the game:
        Until the snake is smaller than 3 (inc. head) it will grow, even if there's no
        food available.

        Args:
            next_step (NextStep): Direction for the next step.
            is_food_available (bool, optional): Is there currenlty food beneath the
                snakes head? Defaults to False.

        Returns:
            Snake: Brand new snake how it would look like in the future after the next step.
        """
        is_baby_snake = len(self) < 3
        if is_baby_snake:
            is_food_available = True
        future_snake: Snake = copy.deepcopy(self)
        future_head_position: Position = self._calc_future_head_position(next_step)
        self._add_future_head_to_future_snake(future_snake, future_head_position)
        if not is_food_available:
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

    def is_dangerous(self, other_snake: "Snake") -> bool:
        """Check if my snake's head collides with other snake badly.

        If my snake collides with the other's snake body I will die (-> dangerous).
        If my snake collides with the other's snake head it depends:
        - the longer snake survives
        - if both snakes have same lenght, both snakes will die.

        Hint: Can be combined with calcualte_future_snake.
        """
        if self.head == other_snake.head:
            if len(self) == len(other_snake):
                return True
            if len(self) > len(other_snake):
                return False
            else:
                return True
        if self.head in other_snake.body_without_head:
            return True
        else:
            return False

    def will_bite_itself(self, next_step: NextStep, is_food_available: bool) -> bool:
        """Will this snake byte itself after the next step (depending from available food now)?

        Args:
            next_step (NextStep)
            is_food_available (bool): referes to current moment and not to the future.
                Food is eaten before next move.
        """
        future_me = self.calculate_future_snake(next_step, is_food_available)
        if future_me.head in future_me.body_without_head:
            return True
        else:
            return False


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

    def calculate_future_board(self) -> "Board":
        """Calculate how the board could look like in the next turn.

        Deterministic is the body of all snakes.
        Unclear is the position of their heads.

        My own snake will not be included in the returned board.

        This method will include all possible snakes,
        "impossible snakes" will be removed.

        All possible head positions are included (pessimistic approach).
        All "eaten" food from the current turn will be removed.

        """
        board_of_possible_future = self._get_board_copy_without_snakes()
        self._remove_eaten_food(board_of_possible_future)
        self._add_other_snakes_of_future_that_dont_bite_itself(board_of_possible_future)
        self._remove_snakes_running_into_walls(board_of_possible_future)
        self._remove_snakes_killed_by_others(board_of_possible_future)
        return board_of_possible_future

    def _get_board_copy_without_snakes(self) -> "Board":
        board_of_possible_future = copy.deepcopy(self)
        board_of_possible_future.all_snakes = {}
        return board_of_possible_future

    def _remove_eaten_food(self, board_of_possible_future: "Board"):
        for position, snake in self.all_snakes.items():
            if self._is_food_available(snake):
                board_of_possible_future.food.remove(position)

    def _add_other_snakes_of_future_that_dont_bite_itself(
        self,
        board_of_possible_future: "Board",
    ):
        """Add all possible snakes to the board (read on details!).

        - All, but not my own snake. I want to add my own snake later on,
        after I can see the board of all possibilities.
        - There are up to 4 snake-copies in the future board for every
        original snake, 1 for every direction (as long as it doesn't bite itself)
        """
        for snake in self.all_snakes.values():
            # My own snake shall not (yet) be part of the
            # future board of possibilities
            if snake == self.my_snake:
                continue
            all_possible_steps = (
                NextStep.UP,
                NextStep.DOWN,
                NextStep.RIGHT,
                NextStep.LEFT,
            )
            for next_step in all_possible_steps:
                if snake.will_bite_itself(next_step, self._is_food_available(snake)):
                    continue
                future_snake = snake.calculate_future_snake(next_step)
                board_of_possible_future.all_snakes[future_snake.head] = future_snake

    def _is_food_available(self, snake: Snake):
        return snake.head in self.food

    def _remove_snakes_running_into_walls(self, board_of_possible_future: "Board"):
        board_of_possible_future.all_snakes = {
            head: snake
            for head, snake in board_of_possible_future.all_snakes.items()
            if not self.is_wall(head)
        }

    def _remove_snakes_killed_by_others(
        self,
        board_of_possible_future: "Board",
    ):
        """All snakes that are *defenitely* killed by another snake are removed.

        What means 'definitely'? Based on current position and food the body
        of every snake in the future step is deterministic. But the snake's heads
        are not and depend from individual decisions of the snakes.
        Therefore the method will *not* remove snakes that might be killed due to
        head collisions, but only snake that are killed because they bite
        into another body (excl. head).
        """
        future_snakes = list(board_of_possible_future.all_snakes.values())
        while future_snakes:
            snake_for_checking_if_save = future_snakes.pop()
            for possibly_threatening_snake in future_snakes:
                # Can't use snake.is_dangerous here, because that would include
                # kills based on head collision.
                if self._is_snake_definitely_killed(
                    snake_for_checking_if_save, possibly_threatening_snake
                ):
                    del board_of_possible_future.all_snakes[
                        snake_for_checking_if_save.head
                    ]
                    break

    def _is_snake_definitely_killed(
        self,
        snake_for_checking_if_save: Snake,
        possibly_threatening_snake: Snake,
    ):
        """Ignore head collisions!"""
        if (
            snake_for_checking_if_save.head
            in possibly_threatening_snake.body_without_head
        ):
            return True
        else:
            return False
