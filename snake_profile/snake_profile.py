import json
import sys
import time
from pathlib import Path

from battle_snake.interactor import MoveDecision

test_requests_file_name = "test_request_move_me_3.json"
sample_request = Path.cwd().parent / "tests" / test_requests_file_name
if not sample_request.exists():
    sample_request = Path.cwd() / "tests" / test_requests_file_name
if not sample_request.exists():
    print(
        "You are in the wrong directory. Move to dir 'snake_profile' or to its parent dir, please."
    )
    sys.exit(1)
request = json.loads(sample_request.read_text())
start = time.perf_counter()
md = MoveDecision(request)
decision = md.decide()
print(time.perf_counter() - start)
print(decision)
