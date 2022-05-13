import logging
import random
import time
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
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
    This controls your Battlesnake appearance and author.
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
            self.future_board.next_turn()
        logging.info(f"Posisition of my snake: {self.board.my_snake}")
        decision = self.tactics.decide()
        logging.info(f"Decision for next step: {decision}")
        return decision


class MyFutureHistory(Recorder):
    def __init__(self):
        self._food_after_steps: dict[  # type: ignore
            NextStep, Optional[int]
        ] = self._init_food_dict()
        self._count_alive_after_steps: dict[  # type: ignore
            NextStep, dict[int, int]
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
            first_step = snake.get_my_first_step()
            self._check_for_food(snake)
            self._increment_snake_alive_counter(first_step)

    def _increment_snake_alive_counter(self, first_step):
        turn_no = self._current_future_board.simulated_turns
        amount = self._count_alive_after_steps[first_step].get(turn_no, 0)
        self._count_alive_after_steps[first_step][turn_no] = amount + 1

    def _check_for_food(self, snake):
        first_step = snake.get_my_first_step()
        food_available = self._current_future_board.is_food_available_for(snake)
        if self._was_no_food_in_this_direction_until_now(first_step) and food_available:
            self._food_after_steps[
                first_step
            ] = self._current_future_board.simulated_turns

    def _was_no_food_in_this_direction_until_now(self, first_step):
        return self._food_after_steps[first_step] is None

    def found_food_after_how_many_steps(self, first_step: NextStep) -> Optional[int]:
        return self._food_after_steps[first_step]

    def all_snakes_definitely_dead_after_how_many_steps(
        self, first_step: NextStep
    ) -> int:
        counter_first_step = self._count_alive_after_steps[first_step]
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
