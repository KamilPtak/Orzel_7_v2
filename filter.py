from collections import deque

class MovingAverageFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def add_sample(self, sample):
        self.buffer.append(sample)

    def get_average(self):
        if not self.buffer:
            return None 
        return sum(self.buffer) / len(self.buffer)


