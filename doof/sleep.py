class Sleep:
    def __init__(self, move):
        self.move = move
        self.sleeping = True

    def bop(self):
        if self.sleeping:
            self.wake()
    
    def sleep(self):
        if self.sleeping:
            return

        self.sleeping = True
        self.move.move_camera(0, 45)

    def wake(self):
        if not self.sleeping:
            return

        self.sleeping = False
        self.move.move_camera(0, -45)


