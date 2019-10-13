import random
import time

MAX_MOVE = 10
MOVE_TIME = 3

class Search:
    def __init__(self, move):
        self.move = move

    def search(self):
        # Only search once a second
        if self.move.move_complete_at > time.time() - MOVE_TIME:
            return

        print("searching")

        self.move.change_both(
            random.randint(-MAX_MOVE, MAX_MOVE),
            random.randint(-MAX_MOVE, MAX_MOVE)
        )


