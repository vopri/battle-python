# [Battlesnake](http://play.battlesnake.com?utm_source=github&utm_medium=readme&utm_campaign=python_starter&utm_content=homepage) and Python

![Battlesnake Logo](https://media.battlesnake.com/social/StarterSnakeGitHubRepos_Python.png)

I've used the basic implementation of the [Battlesnake API](https://docs.battlesnake.com/references/api) in Python as a starting point.

## Strategy and Tactics of my Battlesnake

My strategy is to simulate several turns of the game and to track all possible snakes, that could survive on the board. "Could" means that I'll take an optimistic approach, to make decisions for my own snake on the "safe side". I choose the first step of my "FutureSnake" that will have survived for the longest time. If there are several possiblities I choose the first step that will lead me to food early. Collisions with bigger snake's heads will be avoided - at least for the first step.

## Local installation

Local installation can be done using [poetry](https://python-poetry.org/). All further packages for [testing](https://docs.pytest.org/en/7.1.x/) will be installed on the way.

## Technologies Used

* [Python3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)

## Some Basic Diagrams

* [Logical Flow](https://github.com/vopri/battle-python/blob/main/docs/Sequence.png)
* [Package Overview](https://github.com/vopri/battle-python/blob/main/docs/packages.png)
* [More Detailed Class Diagram](https://github.com/vopri/battle-python/blob/main/docs/classes.png)
