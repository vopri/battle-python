import time
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import NewType, Optional

from battle_snake.entities import (
    Board,
    FutureBoard,
    FutureSnake,
    NextStep,
    PossibleFutureBoard,
)


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


class MoveDecision:
    """Decision maker for the next move of my snake."""

    def __init__(self, game_request: dict):
        self._start_time: int = time.perf_counter_ns()
        self._history = MySnakeHistory()
        self.board: Board = Board.from_dict(game_request)
        self.future_board: FutureBoard = FutureBoard(self.board)

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""
        my_survivors = self._simulate_survivors()
        if my_survivors is None:
            return self._die_like_a_snake()
        elif self._only_one_survivor_left(my_survivors):
            chosen_first_step = my_survivors.pop().get_my_first_step()
        else:
            chosen_first_step = self._choose_optimal_first_step(my_survivors)
        return chosen_first_step

    def _simulate_survivors(self) -> None | set[FutureSnake]:
        my_survivors: Optional[set[FutureSnake]] = None
        self._save_my_snakes_history()
        while not self._time_is_over():
            my_survivors_of_this_turn = self.future_board.get_my_survived_snakes()
            if self._no_survivors_left(my_survivors_of_this_turn):
                break
            my_survivors = my_survivors_of_this_turn
            if self._only_one_survivor_left(my_survivors_of_this_turn):
                break
            else:
                self.future_board.next_turn()
                self._save_my_snakes_history()
        print(self.future_board.simulated_turns)
        return my_survivors

    def _save_my_snakes_history(self):
        my_snakes = self.future_board.get_my_survived_snakes()
        turn_no: int = self.future_board.simulated_turns
        for snake in my_snakes:
            first_step = snake.get_my_first_step()
            if turn_no == 1:
                self._save_head_collision_risk(snake, first_step)
            self._save_if_food_available(turn_no, snake, first_step)

    def _save_head_collision_risk(self, snake, first_step):
        risk = self.future_board.calc_head_collision_risk_for(snake)
        self._history.head_collision_risk_first_step[first_step] = risk

    def _save_if_food_available(
        self, turn_no: int, snake: FutureSnake, first_step: NextStep
    ):
        if self._not_yet_food_found_for_this_variant(
            first_step
        ) and self.future_board.is_food_available_for(snake):
            self._history.food_after_how_many_steps[first_step] = turn_no

    def _not_yet_food_found_for_this_variant(self, first_step: NextStep):
        return first_step not in self._history.food_after_how_many_steps.values()

    def _time_is_over(self) -> bool:
        stop_latest_after_ns = 1_000_000 * 100
        return time.perf_counter_ns() - self._start_time > stop_latest_after_ns

    def _no_survivors_left(self, my_survivors_of_this_turn):
        return len(my_survivors_of_this_turn) == 0

    def _die_like_a_snake(self):
        return NextStep.UP

    def _only_one_survivor_left(self, my_survivors_of_this_turn):
        return len(my_survivors_of_this_turn) == 1

    def _choose_optimal_first_step(self, my_survivors: set[FutureSnake]) -> NextStep:
        first_step_of_survivors: set[NextStep] = {
            my_survivor.get_my_first_step() for my_survivor in my_survivors
        }
        first_step_of_min_risk_survivors = first_step_of_survivors.intersection(
            self._history.get_steps_with_min_head_collision_risk()
        )
        first_step_of_min_risk_survivors = sorted(
            first_step_of_min_risk_survivors,
            key=lambda next_step: self._history.food_after_how_many_steps.get(
                next_step, 1_000
            ),
        )
        return first_step_of_min_risk_survivors[0]


class MySnakeHistory:
    def __init__(self):
        self.head_collision_risk_first_step: dict[NextStep, float] = dict()
        self.can_kill_snake_in_first_step: dict[NextStep, bool] = dict()
        self.food_after_how_many_steps: dict[NextStep, int] = dict()

    def get_steps_with_min_head_collision_risk(self) -> set[NextStep]:
        min_risk = min(self.head_collision_risk_first_step.values())
        return {
            next_step
            for next_step in self.head_collision_risk_first_step.keys()
            if self.head_collision_risk_first_step[next_step] == min_risk
        }


class MyFutureHistory:
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
        for max_steps in range(7, 0, -1):
            surviors_first_steps = self._find_survivors(max_steps)
            if surviors_first_steps:
                break
        food_after: dict[int, NextStep] = dict()
        for step in surviors_first_steps:
            amount_of_steps = self._history.found_food_after_how_many_steps(step)
            if amount_of_steps is not None:
                food_after[amount_of_steps] = step
        shortest_way_to_food = min(food_after.keys())
        return food_after[shortest_way_to_food]

    def _find_survivors(self, max_steps: int):
        return {
            step
            for step in NextStep
            if self._history.all_snakes_definitely_dead_after_how_many_steps(step)
            > max_steps
        }
