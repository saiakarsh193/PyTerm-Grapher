import numpy as np

class Buffer():
    def __init__(self, data, rows, cols, lx, hx, ly, hy):
        if data is None:
            data = np.zeros(shape=(rows, cols), dtype=int)
        self.data = data
        self.rows = rows
        self.cols = cols
        self.lx = lx
        self.hx = hx
        self.ly = ly
        self.hy = hy