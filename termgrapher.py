from typing import Type
import numpy as np
import json

from numpy.lib.arraysetops import isin
from numpy.lib.function_base import insert
from buffer import Buffer

class termGrapher():
    def __init__(self):
        self.defaults = {"rows": 10, "cols": 10, "lx": -10, "hx": 10, "ly": -10, "hy": 10}
        self.new(rows=self.defaults["rows"], cols=self.defaults["cols"], lx=self.defaults["lx"], hx=self.defaults["hx"], ly=self.defaults["ly"], hy=self.defaults["hy"])

    def new(self, rows, cols, lx, hx, ly, hy, data=None):
        self.set(Buffer(data=data, rows=rows, cols=cols, lx=lx, hx=hx, ly=ly, hy=hy))
        return self.get()
    
    def get(self):
        return self.buffer
    
    def set(self, figure):
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        self.buffer = figure

    def clear(self, figure=None):
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        figure.data *= 0

    def graph(self, comparator, figure=None):
        if not(hasattr(comparator, '__call__') and comparator.__name__ == "<lambda>"):
            raise ValueError("Given comparator is not a lambda function")
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        precomp = np.fromfunction(lambda i, j: comparator(figure.lx + (j / figure.cols) * (figure.hx - figure.lx), figure.hy + (i / figure.rows) * (figure.ly - figure.hy)), (figure.rows + 1, figure.cols + 1))
        precomp = np.where(precomp >= 0, 1, -1)
        precomp = precomp[0: figure.rows, 0: figure.cols] + precomp[1: figure.rows + 1, 0: figure.cols] + precomp[0: figure.rows, 1: figure.cols + 1] + precomp[1: figure.rows + 1, 1: figure.cols + 1]
        precomp = np.where(np.abs(precomp) == 4, 0, 1)
        precomp += figure.data
        precomp = np.where(precomp > 0, 1, 0)
        figure.data = precomp

    def plot(self, x, y, figure=None):
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        assert type(x) == type(y), "Type mismatch"
        if(isinstance(x, np.ndarray) and isinstance(y, np.ndarray)):
            assert x.ndim == 1 and y.ndim == 1, "Dimension of numpy array should be 1"
            assert x.shape[0] == y.shape[0], "Length of numpy arrays do not match"
            assert (x.dtype in ["int", "float"]) and (y.dtype in ["int", "float"]), "Numpy arrays contain invalid values"
            x = x.tolist()
            y = y.tolist()
        elif(isinstance(x, list) and isinstance(y, list)):
            assert len(x) == len(y), "Length of lists do not match"
            assert all(isinstance(v, (int, float)) for v in x) and all(isinstance(v, (int, float)) for v in y), "Lists contain invalid values"
        else:
            raise TypeError("Invalid data type values given")
        for ind in range(len(x) - 1):
            col1 = int(((x[ind] - figure.lx) / (figure.hx - figure.lx)) * (figure.cols - 1))
            row1 = int(((y[ind] - figure.hy) / (figure.ly - figure.hy)) * (figure.rows - 1))
            col2 = int(((x[ind + 1] - figure.lx) / (figure.hx - figure.lx)) * (figure.cols - 1))
            row2 = int(((y[ind + 1] - figure.hy) / (figure.ly - figure.hy)) * (figure.rows - 1))
            # Implement DDA for line joining
    
    def scatter(self, x, y, figure=None):
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        assert type(x) == type(y), "Type mismatch"
        if(isinstance(x, np.ndarray) and isinstance(y, np.ndarray)):
            assert x.ndim == 1 and y.ndim == 1, "Dimension of numpy array should be 1"
            assert x.shape[0] == y.shape[0], "Length of numpy arrays do not match"
            assert (x.dtype in ["int", "float"]) and (y.dtype in ["int", "float"]), "Numpy arrays contain invalid values"
            x = x.tolist()
            y = y.tolist()
        elif(isinstance(x, list) and isinstance(y, list)):
            assert len(x) == len(y), "Length of lists do not match"
            assert all(isinstance(v, (int, float)) for v in x) and all(isinstance(v, (int, float)) for v in y), "Lists contain invalid values"
        else:
            raise TypeError("Invalid data type values given")
        for ind, item in enumerate(x):
            col = int(((x[ind] - figure.lx) / (figure.hx - figure.lx)) * (figure.cols - 1))
            row = int(((y[ind] - figure.hy) / (figure.ly - figure.hy)) * (figure.rows - 1))
            if(col >= 0 and col < figure.cols and row >= 0 and row < figure.rows):
                figure.data[row, col] = 1

    def show(self, figure=None):
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        prbuf = " " + "".join(["__"] * figure.cols) + " \n"
        for i in range(figure.rows):
            prbuf += "|"
            for j in range(figure.cols):
                prbuf += "  " if figure.data[i, j] == 0 else "* "
            prbuf += "|\n"
        prbuf += " " + "".join(["--"] * figure.cols) + " "
        print(prbuf)

    def save(self, filename="figure", figure=None):
        if figure is None:
            figure = self.buffer
        if not isinstance(figure, Buffer):
            raise ValueError("Given figure is not a buffer object")
        cbuffer = self._compressBuffer(figure.data.tolist(), figure.rows, figure.cols)
        self._dumpJSON({"cbuffer": cbuffer, "rows": figure.rows, "cols": figure.cols, "lx": figure.lx, "hx": figure.hx, "ly": figure.ly, "hy": figure.hy}, path="./" + filename)
    
    def _compressBuffer(self, data, rows, cols):
        cbuff = [[data[0][0], 0]]
        for i in range(rows):
            for j in range(cols):
                if(cbuff[-1][0] == data[i][j]):
                    cbuff[-1][1] += 1
                else:
                    cbuff.append([data[i][j], 1])
        return cbuff

    def _dumpJSON(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)
        
    def load(self, path):
        data = self._loadJSON(path)
        nbuffer = self._decompressBuffer(data["cbuffer"], data["rows"], data["cols"])
        return self.new(rows=data["rows"], cols=data["cols"], lx=data["lx"], hx=data["hx"], ly=data["ly"], hy=data["hy"], data=np.array(nbuffer))

    def _decompressBuffer(self, data, rows, cols):
        nbuff = [[0] * cols for _ in range(rows)]
        pos = 0
        ctr = 0
        for i in range(rows):
            for j in range(cols):
                nbuff[i][j] = data[pos][0]
                ctr += 1
                if(ctr == data[pos][1]):
                    pos += 1
                    ctr = 0
        return nbuff
    
    def _loadJSON(self, path):
        with open(path, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    tg = termGrapher()
    fig = tg.new(40, 40, -5, 5, -25, 25)
    tg.graph(lambda x, y: y)
    tg.graph(lambda x, y: 0.2 * y - np.sin(x))
    tg.show(fig)

