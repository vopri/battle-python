import time
from copy import deepcopy
from typing import Optional

from battle_snake.entities import Board, FutureBoard, FutureSnake, NextStep


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
        self.board: Board = Board.from_dict(game_request)
        self.future_board: FutureBoard = FutureBoard(self.board)
        self._copy_of_first_future_board: FutureBoard = deepcopy(self.future_board)

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""
        my_survivors = self._simulate_survivors()
        if my_survivors is None:
            return self._die_like_a_snake()
        elif self._only_one_survivor_left(my_survivors):
            chosen_snake = my_survivors.pop()
        else:
            chosen_snake = self._choose_optimal_survivor(my_survivors)
        return chosen_snake.get_my_first_step()

    def _simulate_survivors(self) -> None | set[FutureSnake]:
        max_turns_to_check_ahead = 20
        my_survivors: Optional[set[FutureSnake]] = None
        for _ in range(max_turns_to_check_ahead):
            if self._time_is_over():
                break
            my_survivors_of_this_turn = self.future_board.get_my_survived_snakes()
            if self._no_survivors_left(my_survivors_of_this_turn):
                break
            my_survivors = my_survivors_of_this_turn
            if self._only_one_survivor_left(my_survivors_of_this_turn):
                break
            else:
                self.future_board.next_turn()
        print(self.future_board._simulated_turns)
        return my_survivors

    def _time_is_over(self) -> bool:
        stop_latest_after_ns = 1_000_000 * 120
        return time.perf_counter_ns() - self._start_time > stop_latest_after_ns

    def _no_survivors_left(self, my_survivors_of_this_turn):
        return len(my_survivors_of_this_turn) == 0

    def _die_like_a_snake(self):
        return NextStep.UP

    def _only_one_survivor_left(self, my_survivors_of_this_turn):
        return len(my_survivors_of_this_turn) == 1

    def _choose_optimal_survivor(self, my_survivors):
        grand_mothers_of_survivors = self._get_first_ancestors_of_survivors(
            my_survivors
        )
        my_survivors_sorted_by_risk_of_head_collision = sorted(
            grand_mothers_of_survivors,
            key=self.sort_by_collision_risk_and_available_food,
            reverse=True,
        )
        chosen_snake = my_survivors_sorted_by_risk_of_head_collision.pop()
        return chosen_snake

    def _get_first_ancestors_of_survivors(self, my_survivors):
        return {
            snake.find_first_future_snake_of_my_ancestors() for snake in my_survivors
        }

    def sort_by_collision_risk_and_available_food(self, snake: FutureSnake):
        return (
            self._copy_of_first_future_board.calc_head_collision_risk_for(snake),
            # looks funny, but False (0) comes before True (1)
            not self._copy_of_first_future_board.is_food_available_for(snake),
        )
