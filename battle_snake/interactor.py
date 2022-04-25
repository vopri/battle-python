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
        self.board: Board = Board.from_dict(game_request)
        self.future_board: FutureBoard = FutureBoard(self.board)

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""

        my_survivors = self.future_board.get_my_survived_snakes()
        is_no_survivor = len(my_survivors) == 0
        if is_no_survivor:
            return self._die_like_a_snake()
        my_survivors_sorted_by_risk_of_head_collision = sorted(
            my_survivors,
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
