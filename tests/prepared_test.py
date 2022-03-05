"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python src/tests.py -v

"""
import unittest

from battle_snake import logic
from battle_snake.entities import NextStep


class AvoidNeckTest(unittest.TestCase):
    def test_avoid_neck_all(self):
        # Arrange
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 5}, {"x": 5, "y": 5}]
        possible_moves = [NextStep.UP, NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]

        # Act
        result_moves = logic._avoid_my_neck(test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(possible_moves, result_moves)

    def test_avoid_neck_left(self):
        # Arrange
        test_body = [{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}]
        possible_moves = [NextStep.UP, NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]
        expected = ["up", "down", "right"]
        expected = [NextStep.UP, NextStep.DOWN, NextStep.RIGHT]

        # Act
        result_moves = logic._avoid_my_neck(test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_right(self):
        # Arrange
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}]
        possible_moves = [NextStep.UP, NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]
        expected = ["up", "down", "left"]
        expected = [NextStep.UP, NextStep.DOWN, NextStep.LEFT]

        # Act
        result_moves = logic._avoid_my_neck(test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_up(self):
        # Arrange
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}]
        possible_moves = [NextStep.UP, NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]
        expected = [NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]

        # Act
        result_moves = logic._avoid_my_neck(test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_down(self):
        # Arrange
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}]
        possible_moves = [NextStep.UP, NextStep.DOWN, NextStep.LEFT, NextStep.RIGHT]
        expected = ["up", "left", "right"]
        expected = [NextStep.UP, NextStep.LEFT, NextStep.RIGHT]

        # Act
        result_moves = logic._avoid_my_neck(test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)


if __name__ == "__main__":
    unittest.main()
