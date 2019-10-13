class Sleep:
    def __init__(self, move):
        self.move = move
        self.sleeping = True

    def bop(self):
        if self.sleeping:
            self.wake()
        else:
            self.sleep()
    
    def sleep(self):
        if self.sleeping:
            return

        print("I sleep")

        self.sleeping = True
        self.move.move_both(0, 45)

    def wake(self):
        if not self.sleeping:
            return

        print("Real shit?")

        self.sleeping = False
        self.move.move_both(0, -45)


