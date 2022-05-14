import logging
import random
import time
from typing import NewType, Optional

from battle_snake.entities import (
    Board,
    FutureSnake,
    NextStep,
    PossibleFutureBoard,
    Recorder,
)

logging.basicConfig(encoding="utf-8", level=logging.INFO)


def get_info() -> dict:
    """
    Battlesnake appearance and author.
    For customization options, see https://docs.battlesnake.com/references/personalization
    """
    return {
        "apiversion": "1",
        "author": "vopri",
        "color": "#ff9900",
        "head": "fang",
        "tail": "hook",
    }


FORECAST_DEPTH = 8


class MoveDecision:
    """Decision maker for the next move of my snake."""

    def __init__(self, game_request: dict):
        self._start_time: int = time.perf_counter_ns()
        self.board: Board = Board.from_dict(game_request)
        self.future_board: PossibleFutureBoard = PossibleFutureBoard(self.board)
        self._history = MyFutureHistory()
        self.future_board.register_recorder(self._history)
        self.tactics = Tactics(self._history)

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""
        for _ in range(FORECAST_DEPTH - 1):
            if self._is_ready_for_decision():
                break
            self.future_board.next_turn()
        logging.info(f"Posisition of my snake: {self.board.my_snake}")
        decision = self.tactics.decide()
        logging.info(f"Decision for next step: {decision}")
        return decision

    def _is_ready_for_decision(self) -> bool:
        survivors = self.future_board.get_my_survived_snakes()
        first_steps = {snake.get_my_first_step() for snake in survivors}
        return len(first_steps) < 2


AmountOfSteps = NewType("AmountOfSteps", int)
AmountOfSnakesAlive = NewType("AmountOfSnakesAlive", int)


class MyFutureHistory(Recorder):
    """Recorder of information of my snake generated by simulations from PossibleFutureBoard."""

    def __init__(self):
        self._found_first_food_after_n_steps: dict[  # type: ignore
            NextStep, Optional[AmountOfSteps]
        ] = self._init_food_dict()
        self._counter_of_snakes_alive_after_n_steps: dict[  # type: ignore
            NextStep, dict[AmountOfSteps, AmountOfSnakesAlive]
        ] = self._init_count_alive_dict()
        self._current_future_board: PossibleFutureBoard = None  # type: ignore

    def _init_food_dict(self) -> dict[NextStep, None]:
        return {
            NextStep.UP: None,
            NextStep.DOWN: None,
            NextStep.LEFT: None,
            NextStep.RIGHT: None,
        }

    def _init_count_alive_dict(self) -> dict[NextStep, dict]:
        return {
            NextStep.UP: dict(),
            NextStep.DOWN: dict(),
            NextStep.LEFT: dict(),
            NextStep.RIGHT: dict(),
        }

    def save(self, future_board: PossibleFutureBoard) -> None:
        self._current_future_board = future_board
        for snake in future_board.get_my_survived_snakes():
            self._check_for_food(snake)
            self._increment_snake_alive_counter(snake)

    def _check_for_food(self, snake: FutureSnake):
        first_step = snake.get_my_first_step()
        is_food_available = self._current_future_board.is_food_available_for(snake)
        is_no_food_yet = self._was_no_food_found_in_this_direction_until_now(snake)
        if is_no_food_yet and is_food_available:
            self._save_food_info(first_step)

    def _was_no_food_found_in_this_direction_until_now(self, snake: FutureSnake):
        first_step = snake.get_my_first_step()
        return self._found_first_food_after_n_steps[first_step] is None

    def _save_food_info(self, first_step):
        self._found_first_food_after_n_steps[first_step] = AmountOfSteps(
            self._current_future_board.simulated_turns
        )

    def _increment_snake_alive_counter(self, snake: FutureSnake):
        first_step = snake.get_my_first_step()
        amount_of_steps = AmountOfSteps(self._current_future_board.simulated_turns)
        amount_of_snakes_alive = self._counter_of_snakes_alive_after_n_steps[
            first_step
        ].get(amount_of_steps, 0)
        self._counter_of_snakes_alive_after_n_steps[first_step][
            amount_of_steps
        ] = AmountOfSnakesAlive(amount_of_snakes_alive + 1)

    def found_food_after_how_many_steps(self, first_step: NextStep) -> Optional[int]:
        return self._found_first_food_after_n_steps[first_step]

    def all_snakes_definitely_dead_after_how_many_steps(
        self, first_step: NextStep
    ) -> int:
        counter_first_step = self._counter_of_snakes_alive_after_n_steps[first_step]
        if len(counter_first_step.keys()) == 0:
            return 1
        return max(counter_first_step.keys()) + 1


class Tactics:
    def __init__(self, history: MyFutureHistory):
        self._history = history

    def decide(self) -> NextStep:
        surviors_first_steps = set()
        for max_steps in range(FORECAST_DEPTH, 0, -1):
            surviors_first_steps = self._find_survivors(max_steps)
            if surviors_first_steps:
                break
        food_after: dict[int, NextStep] = dict()
        for step in surviors_first_steps:
            amount_of_steps = self._history.found_food_after_how_many_steps(step)
            if amount_of_steps is not None:
                food_after[amount_of_steps] = step
        if food_after:
            shortest_way_to_food = min(food_after.keys())
            return food_after[shortest_way_to_food]
        elif surviors_first_steps:
            return random.choice(list(surviors_first_steps))
        else:
            # die like a snake!
            return NextStep.UP

    def _find_survivors(self, max_steps: int):
        return {
            step
            for step in NextStep
            if self._history.all_snakes_definitely_dead_after_how_many_steps(step)
            > max_steps
        }
