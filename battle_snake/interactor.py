import logging
import random
import time
from typing import Optional

from battle_snake.entities import (
    AmountOfSnakesAlive,
    AmountOfSteps,
    Board,
    FirstStep,
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


FORECAST_DEPTH = 7


class MoveDecision:
    """Decision maker for the next move of my snake."""

    def __init__(self, game_request: dict):
        self._start_time: int = time.perf_counter_ns()
        self.board: Board = Board.from_dict(game_request)
        self.future_board: PossibleFutureBoard = PossibleFutureBoard(self.board)
        self._history = MyFutureHistory()
        self.future_board.register_recorder(self._history)
        self.tactics = Tactics(self._history, self.board)

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""
        self._calculate_simulation()
        logging.info(f"Posisition of my snake: {self.board.my_snake}")
        decision = self.tactics.decide()
        logging.info(f"Decision for next step: {decision}")
        return decision

    def _calculate_simulation(self):
        for _ in range(FORECAST_DEPTH - 1):
            if self._is_ready_for_decision():
                break
            self.future_board.next_turn()

    def _is_ready_for_decision(self) -> bool:
        survivors = self.future_board.get_my_survived_snakes()
        first_steps = {snake.get_my_first_step() for snake in survivors}
        return len(first_steps) < 2


class MyFutureHistory(Recorder):
    """Recorder of information of my snake generated by simulations from PossibleFutureBoard."""

    def __init__(self):
        self._counter_of_snakes_alive_after_n_steps: dict[
            FirstStep, dict[AmountOfSteps, AmountOfSnakesAlive]
        ] = {FirstStep(first_step): dict() for first_step in NextStep}
        self._found_first_food_after_n_steps: dict[
            FirstStep, Optional[AmountOfSteps]
        ] = {FirstStep(first_step): None for first_step in NextStep}

        self._current_future_board: PossibleFutureBoard = None  # type: ignore
        self._dangerous_snake_first_step: dict[FirstStep, bool] = dict()

    def save(self, future_board: PossibleFutureBoard) -> None:
        """Save interesting information of current state of PossibleFutureBoard"""
        self._current_future_board = future_board
        for my_snake in future_board.get_my_survived_snakes():
            self._increment_snake_alive_counter(my_snake)
            self._check_for_dangerous_snake_in_first_step(my_snake)
            self._check_for_food(my_snake)

    def _increment_snake_alive_counter(self, my_snake: FutureSnake):
        first_step = FirstStep(my_snake.get_my_first_step())
        amount_of_steps = AmountOfSteps(self._current_future_board.simulated_turns)
        amount_of_snakes_alive = (
            self._get_amount_of_snakes_alive_for_first_step_and_current_turn(
                first_step, amount_of_steps
            )
        )
        self._counter_of_snakes_alive_after_n_steps[first_step][
            amount_of_steps
        ] = AmountOfSnakesAlive(amount_of_snakes_alive + 1)

    def _get_amount_of_snakes_alive_for_first_step_and_current_turn(
        self, first_step: FirstStep, amount_of_steps: AmountOfSteps
    ) -> AmountOfSnakesAlive:
        return AmountOfSnakesAlive(
            self._counter_of_snakes_alive_after_n_steps[first_step].get(
                amount_of_steps, 0
            )
        )

    def _check_for_dangerous_snake_in_first_step(self, my_snake: FutureSnake):
        if self._current_future_board.simulated_turns > 1:
            return
        is_danger_ahead = (
            self._current_future_board.does_my_snake_bite_or_collide_with_another_snake(
                my_snake
            )
        )
        first_step = my_snake.get_my_first_step()
        self._dangerous_snake_first_step[FirstStep(first_step)] = is_danger_ahead

    def _check_for_food(self, my_snake: FutureSnake):
        first_step = my_snake.get_my_first_step()
        is_food_available = self._current_future_board.is_food_available_for(my_snake)
        is_no_food_yet = self._was_no_food_found_in_this_direction_until_now(my_snake)
        if is_no_food_yet and is_food_available:
            self._save_food_info(first_step)

    def _was_no_food_found_in_this_direction_until_now(self, my_snake: FutureSnake):
        first_step = my_snake.get_my_first_step()
        return self._found_first_food_after_n_steps[FirstStep(first_step)] is None

    def _save_food_info(self, first_step):
        self._found_first_food_after_n_steps[first_step] = AmountOfSteps(
            self._current_future_board.simulated_turns
        )

    def my_snake_found_food_after_how_many_steps(
        self, first_step: NextStep
    ) -> Optional[int]:
        return self._found_first_food_after_n_steps[FirstStep(first_step)]

    def all_my_snakes_definitely_dead_after_how_many_steps(
        self, first_step: FirstStep
    ) -> int:
        counter_first_step = self._counter_of_snakes_alive_after_n_steps[
            FirstStep(first_step)
        ]
        if len(counter_first_step.keys()) == 0:
            return 1
        return max(counter_first_step.keys()) + 1

    def is_dangerous_snake_in_first_step(self, first_step: FirstStep):
        return self._dangerous_snake_first_step[FirstStep(first_step)]


class Tactics:
    def __init__(self, history: MyFutureHistory, board: Board):
        self._history = history
        self._latest_surviors_first_steps: set[FirstStep] = None  # type: ignore
        self._smelt_food: dict[AmountOfSteps, FirstStep] = dict()  # type: ignore
        self._board = board

    def decide(self) -> NextStep:
        """Here's the decision made based on collected data of the simulation"""
        self._init_with_first_steps_of_last_survivors()
        self._try_to_avoid_collision_in_first_step()
        if self._there_is_just_one_possibility():
            logging.info(
                f"There's one step left only: {self._latest_surviors_first_steps}"
            )
            return self._latest_surviors_first_steps.pop()
        if self._there_is_no_way_out():
            logging.info(f"I'm dying ... arghhhh ...")
            return NextStep.UP
        self._try_to_smell_food_on_path()
        if self._i_can_smell_food():
            return self._get_first_step_to_nearest_food()
        # Find food that I can't smell yet
        else:
            for food_pos in self._board.get_food_ordered_by_distance(
                self._board.my_snake.head
            ):
                first_steps_leading_to_food: set[FirstStep] = food_pos[0]
                first_steps_leading_to_food = (
                    self._latest_surviors_first_steps.intersection(
                        first_steps_leading_to_food
                    )
                )
                if len(first_steps_leading_to_food) > 0:
                    first_step = first_steps_leading_to_food.pop()
                    logging.info(
                        f"First secure step leading to food that I couldn't smell: {first_step}"
                    )
                    return first_step

        logging.info(
            f"I'll guess one by luck from, because there's no food securely reachable... {self._latest_surviors_first_steps}"
        )
        return random.choice(list(self._latest_surviors_first_steps))

    def _init_with_first_steps_of_last_survivors(self):
        logging.info("\n" + "New Decision   " + "*" * 30)
        logging.info(
            f"Survivors simulation: {self._history._counter_of_snakes_alive_after_n_steps}"
        )
        self._latest_surviors_first_steps = self._get_first_steps_of_latest_survivor()
        logging.info(f"Latest survivors: {self._latest_surviors_first_steps}")

    def _get_first_steps_of_latest_survivor(self) -> set[FirstStep]:
        surviors_first_steps = set()
        for max_steps in range(FORECAST_DEPTH, 0, -1):
            surviors_first_steps = self._find_survivors(max_steps)
            if surviors_first_steps:
                break
        return surviors_first_steps

    def _find_survivors(self, max_steps: int):
        return {
            direction
            for direction in NextStep
            if self._history.all_my_snakes_definitely_dead_after_how_many_steps(
                FirstStep(direction)
            )
            > max_steps
        }

    def _try_to_avoid_collision_in_first_step(self):
        # If next calc removes to many steps, I want to be able to switch back
        latest_surviors_first_steps_backup = self._latest_surviors_first_steps.copy()
        self._remove_possible_snake_collision_in_first_step()
        if len(self._latest_surviors_first_steps) == 0:
            logging.info(
                "Avoiding collision in first step will be revised..."
                "I will have to take my chances",
            )
            self._latest_surviors_first_steps = latest_surviors_first_steps_backup
        logging.info(
            f"Avoiding collision in first step: {self._latest_surviors_first_steps}"
        )

    def _remove_possible_snake_collision_in_first_step(self):
        if len(self._latest_surviors_first_steps) > 1:
            self._latest_surviors_first_steps = {
                first_step
                for first_step in self._latest_surviors_first_steps
                if not self._history.is_dangerous_snake_in_first_step(
                    FirstStep(first_step)
                )
            }

    def _there_is_just_one_possibility(self) -> bool:
        return len(self._latest_surviors_first_steps) == 1

    def _there_is_no_way_out(self) -> bool:
        return len(self._latest_surviors_first_steps) == 0

    def _get_first_step_to_nearest_food(self) -> FirstStep:
        shortest_way_to_food: AmountOfSteps = min(self._smelt_food.keys())
        logging.info(
            f"Smelling food nearby: {self._smelt_food[shortest_way_to_food]} in {shortest_way_to_food} steps"
        )
        first_step_into_food_direction = self._smelt_food[shortest_way_to_food]
        return first_step_into_food_direction

    def _i_can_smell_food(self) -> bool:
        return len(self._smelt_food) > 0

    def _try_to_smell_food_on_path(self):
        for step in self._latest_surviors_first_steps:
            amount_of_steps = self._history.my_snake_found_food_after_how_many_steps(
                step
            )
            if amount_of_steps is not None:
                self._smelt_food[AmountOfSteps(amount_of_steps)] = FirstStep(step)
