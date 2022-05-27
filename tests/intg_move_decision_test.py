import logging

import pytest
from battle_snake.entities import NextStep
from battle_snake.interactor import MoveDecision


def test_decide_sample_request(sample_move_decision: MoveDecision):
    assert sample_move_decision.decide() == NextStep.UP


def test_decide_solo_1(solo_board_request_1, caplog):
    caplog.set_level(logging.INFO)
    assert MoveDecision(solo_board_request_1).decide() == NextStep.UP


@pytest.mark.parametrize(
    "game_request_name,expected_decision",
    [
        ("sample_request", NextStep.UP),
        ("test_request", NextStep.UP),
        ("test_request_move_me_1", NextStep.RIGHT),
        ("test_request_move_me_2", NextStep.RIGHT),
        ("test_request_move_me_3", NextStep.RIGHT),
    ],
)
def test_decide(
    game_request_name: str,
    expected_decision: NextStep,
    request: pytest.FixtureRequest,
):
    game_request = request.getfixturevalue(game_request_name)
    md = MoveDecision(game_request)
    assert md.decide() == expected_decision
