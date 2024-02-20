# print a load statement with variable number of dots
class Loader:
    def __init__(self, message="Loading", dots=3):
        self.max = dots # max number of dots
        self.direction = 1 # what to increment number by each loop
        self.message = message # starting message
        self.number = 0 # current dot number
        self.width = len(message) + dots

    def loop(self):
        # print load statement
        print(f"\r{self.message}{"." * self.number}{' ' * (self.max - self.number)}", end="")
        # go to next dot number
        if not 0 <= self.number + self.direction <= self.max:
            self.direction *= -1
        self.number += self.direction