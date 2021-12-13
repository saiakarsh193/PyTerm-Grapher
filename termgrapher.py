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
        umap = lambda n, il, ih, fl, fh: fl + ((n - il) / (ih - il)) * (fh - fl)
        for ind in range(len(x) - 1):
            row1 = int(umap(y[ind], figure.hy, figure.ly, 0, figure.rows - 1))
            col1 = int(umap(x[ind], figure.lx, figure.hx, 0, figure.cols - 1))
            row2 = int(umap(y[ind + 1], figure.hy, figure.ly, 0, figure.rows - 1))
            col2 = int(umap(x[ind + 1], figure.lx, figure.hx, 0, figure.cols - 1))
            if(row1 == row2 and col1 == col2):
                if(col1 >= 0 and col1 < figure.cols and row1 >= 0 and row1 < figure.rows):
                    figure.data[row1, col1] = 1
                continue
            ipoints = self._getddapoints(row1, col1, row2, col2)
            for row, col in ipoints:
                if(col >= 0 and col < figure.cols and row >= 0 and row < figure.rows):
                    figure.data[row, col] = 1

    def _autorange(self, a, b):
        return range(a, b + 1) if (a < b) else range(a, b - 1, -1)
    
    def _getddapoints(self, x0, y0, x1, y1):
        points = []
        umap = lambda n, il, ih, fl, fh: fl + ((n - il) / (ih - il)) * (fh - fl)
        if(abs(x0 - x1) >= abs(y0 - y1)):
            for x in self._autorange(x0, x1):
                points.append([x, int(umap(x, x0, x1, y0, y1))])
        else:
            for y in self._autorange(y0, y1):
                points.append([int(umap(y, y0, y1, x0, x1)), y])
        return points
    
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
        umap = lambda n, il, ih, fl, fh: fl + ((n - il) / (ih - il)) * (fh - fl)
        for ind, item in enumerate(x):
            row = int(umap(y[ind], figure.hy, figure.ly, 0, figure.rows - 1))
            col = int(umap(x[ind], figure.lx, figure.hx, 0, figure.cols - 1))
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
