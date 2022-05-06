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

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""

        max_turns_to_check_ahead = 10
        stop_latest_after_ns = 1_000_000 * 300
        backup_of_first_future_board = deepcopy(self.future_board)
        my_survivors: Optional[set[FutureSnake]] = None
        for _ in range(max_turns_to_check_ahead):
            if time.perf_counter_ns() - self._start_time > stop_latest_after_ns:
                break
            my_survivors_of_this_turn = self.future_board.get_my_survived_snakes()
            if len(my_survivors_of_this_turn) == 0:
                break
            my_survivors = my_survivors_of_this_turn
            if len(my_survivors_of_this_turn) == 1:
                break
            else:
                self.future_board.next_turn()
        if my_survivors is None:
            return self._die_like_a_snake()
        elif len(my_survivors) == 1:
            return my_survivors.pop().get_my_first_step()
        else:
            mothers_of_survivors = {
                snake.find_first_future_snake_of_my_ancestors()
                for snake in my_survivors
            }
        self.future_board = backup_of_first_future_board
        my_survivors_sorted_by_risk_of_head_collision = sorted(
            mothers_of_survivors,
            key=self.sort_by_collision_risk_and_available_food,
            reverse=True,
        )
        chosen_snake = my_survivors_sorted_by_risk_of_head_collision.pop()
        return chosen_snake.get_my_first_step()

    def _die_like_a_snake(self):
        return NextStep.UP

    def sort_by_collision_risk_and_available_food(self, snake: FutureSnake):
        return (
            self.future_board.calc_head_collision_risk_for(snake),
            # looks funny, but False (0) comes before True (1)
            not self.future_board.is_food_available_for(snake),
        )
