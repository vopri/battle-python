from battle_snake import interactor
from battle_snake.entities import NextStep, Position, Snake


def test_filter_walls_bottom_left(board_from_file):
    possible_moves = {
        Position(-1, 0): NextStep.LEFT,
        Position(1, 0): NextStep.RIGHT,
        Position(0, 1): NextStep.UP,
        Position(0, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.RIGHT}


def test_filter_walls_bottom_right(board_from_file):
    possible_moves = {
        Position(9, 0): NextStep.LEFT,
        Position(11, 0): NextStep.RIGHT,
        Position(10, 1): NextStep.UP,
        Position(10, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.UP, NextStep.LEFT}


def test_filter_walls_top_left(board_from_file):
    possible_moves = {
        Position(-1, 10): NextStep.LEFT,
        Position(1, 10): NextStep.RIGHT,
        Position(0, 11): NextStep.UP,
        Position(0, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.RIGHT}


def test_filter_walls_top_right(board_from_file):
    possible_moves = {
        Position(9, 10): NextStep.LEFT,
        Position(11, 10): NextStep.RIGHT,
        Position(10, 11): NextStep.UP,
        Position(10, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {NextStep.DOWN, NextStep.LEFT}


def test_filter_walls_top_middle(board_from_file):
    possible_moves = {
        Position(4, 10): NextStep.LEFT,
        Position(6, 10): NextStep.RIGHT,
        Position(5, 11): NextStep.UP,
        Position(5, 9): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_bottom_middle(board_from_file):
    possible_moves = {
        Position(4, 0): NextStep.LEFT,
        Position(6, 0): NextStep.RIGHT,
        Position(5, 1): NextStep.UP,
        Position(5, -1): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.RIGHT,
    }


def test_filter_walls_middle_right(board_from_file):
    possible_moves = {
        Position(9, 5): NextStep.LEFT,
        Position(11, 5): NextStep.RIGHT,
        Position(10, 6): NextStep.UP,
        Position(10, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.LEFT,
        NextStep.DOWN,
    }


def test_filter_walls_middle_left(board_from_file):
    possible_moves = {
        Position(-1, 5): NextStep.LEFT,
        Position(1, 5): NextStep.RIGHT,
        Position(0, 6): NextStep.UP,
        Position(0, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.UP,
        NextStep.RIGHT,
        NextStep.DOWN,
    }


def test_filter_walls_middle(board_from_file):
    possible_moves = {
        Position(4, 5): NextStep.LEFT,
        Position(6, 5): NextStep.RIGHT,
        Position(5, 6): NextStep.UP,
        Position(5, 4): NextStep.DOWN,
    }
    filtered_moves = interactor._avoid_walls(board_from_file, possible_moves)
    assert set(filtered_moves.values()) == {
        NextStep.DOWN,
        NextStep.LEFT,
        NextStep.UP,
        NextStep.RIGHT,
    }


def test_filter_neck_left(snake_right_middle_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_right_middle_short.next_theoretical_head_positions_and_moves(),
        snake_right_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.RIGHT}
    assert set(moves.values()) == expected


def test_filter_neck_right(snake_middle_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_middle_short.next_theoretical_head_positions_and_moves(),
        snake_middle_short,
    )
    assert len(moves) == 3
    expected = {NextStep.UP, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_up(snake_origin: Snake):
    moves = interactor._avoid_my_neck(
        snake_origin.next_theoretical_head_positions_and_moves(),
        snake_origin,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.DOWN, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_filter_neck_down(snake_top_right_short: Snake):
    moves = interactor._avoid_my_neck(
        snake_top_right_short.next_theoretical_head_positions_and_moves(),
        snake_top_right_short,
    )
    assert len(moves) == 3
    expected = {NextStep.RIGHT, NextStep.UP, NextStep.LEFT}
    assert set(moves.values()) == expected


def test_future_snake_right_without_food(
    snake_long: Snake, snake_long_future_right_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.RIGHT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_right_without_food.body_incl_head
    )


def test_future_snake_left_without_food(
    snake_long: Snake, snake_long_future_left_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.LEFT, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_future_left_without_food.body_incl_head
    )


def test_future_snake_up_without_food(
    snake_long: Snake, snake_long_future_up_without_food: Snake
):
    future_snake: Snake = snake_long.calculate_future_snake(
        next_step=NextStep.UP, food=False
    )
    assert (
        future_snake.body_incl_head == snake_long_future_up_without_food.body_incl_head
    )


def test_future_snake_down_without_food(
    snake_long_2: Snake, snake_long_2_future_down_without_food: Snake
):
    future_snake: Snake = snake_long_2.calculate_future_snake(
        next_step=NextStep.DOWN, food=False
    )
    assert (
        future_snake.body_incl_head
        == snake_long_2_future_down_without_food.body_incl_head
    )


def test_avoid_my_body_without_food(snake_in_block: Snake):
    possible_moves = snake_in_block.next_theoretical_head_positions_and_moves()
    filtered_moves = interactor._avoid_my_future_body(
        snake_in_block, possible_moves, my_snake_gets_food=False
    )
    expected_moves = {NextStep.DOWN, NextStep.RIGHT}
    assert set(filtered_moves.values()) == expected_moves


def test_avoid_my_body_with_food(snake_in_block: Snake):
    possible_moves = snake_in_block.next_theoretical_head_positions_and_moves()
    filtered_moves = interactor._avoid_my_future_body(
        snake_in_block, possible_moves, my_snake_gets_food=True
    )
    expected_moves = {NextStep.DOWN}
    assert set(filtered_moves.values()) == expected_moves
