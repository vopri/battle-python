from battle_snake.entities import Position


def test_postion_init():
    orig_pos = {"x": 3, "y": 2}
    pos = Position(**orig_pos)
    assert pos.x == 3
    assert pos.y == 2
    assert pos == Position(3, 2)
