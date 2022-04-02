from battle_snake.entities import Board, FutureBoard, FutureSnake, NextStep, Position


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

    def __init__(self, data: dict):
        self.board: Board = self._init_board(data)
        self.risk_tolerance: float = 0

    def _init_board(self, data: dict) -> Board:
        my_head_pos = Position(**data["you"]["head"])
        return Board(my_head_pos, **data["board"])

    def decide(self) -> NextStep:
        """Find decision for next step for my snake"""

        future_board: FutureBoard = FutureBoard(self.board)
        while self._are_there_no_survivors(future_board) and self.risk_tolerance < 1:
            self._increase_risk_tolerance()
            future_board = FutureBoard(self.board, risk_tolerance=self.risk_tolerance)
        if self._are_there_no_survivors(future_board):
            # die like a snake!
            return NextStep.UP
        best_choice_snake: FutureSnake = self._get_best_choice(future_board)
        return best_choice_snake.get_my_first_step()

    def _increase_risk_tolerance(self):
        self.risk_tolerance += 10

    def _are_there_no_survivors(self, future_board) -> bool:
        return len(future_board.get_my_survived_snakes()) < 1

    def _get_best_choice(self, future_board) -> FutureSnake:
        for snake in future_board.get_my_survived_snakes():
            if future_board.is_food_available_for(snake):
                return snake
        else:
            return future_board.get_my_survived_snakes().pop()
