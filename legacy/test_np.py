import numpy as np
import time

class Buffer():
	def __init__(self, data, rows, cols, lx, hx, ly, hy, compressed=False):
		self.data = data
		self.rows = rows
		self.cols = cols
		self.lx = lx
		self.hx = hx
		self.ly = ly
		self.hy = hy
		self.compressed = compressed

	def size(self):
		return len(self.data) * len(self.data[0])

def getBuffer(rows, cols, lx, hx, ly, hy, comp):
	precomp = np.fromfunction(lambda i, j: comp(lx + (j / cols) * (hx - lx), hy + (i / rows) * (ly - hy)), (rows + 1, cols + 1))
	precomp = np.where(precomp >= 0, 1, -1)
	precomp = precomp[0:rows, 0:cols] + precomp[1:rows + 1, 0:cols] + precomp[0:rows, 1:cols + 1] + precomp[1:rows + 1, 1:cols + 1]
	precomp = np.where(np.abs(precomp) == 4, 0, 1)
	return Buffer(precomp.tolist(), rows, cols, lx, hx, ly, hy)

def printBuffer(buffer):
	assert buffer.compressed == False, "Buffer is compressed, cannot be printed"
	prbuf = " " + "".join(["__"] * buffer.cols) + " \n"
	for i in range(buffer.rows):
		prbuf += "|"
		for j in range(buffer.cols):
			prbuf += "  " if buffer.data[i][j] == 0 else "* "
		prbuf += "|\n"
	prbuf += " " + "".join(["--"] * buffer.cols) + " "
	print(prbuf)

def compressBuffer(buffer):
	assert buffer.compressed == False, "Buffer is already compressed"
	cbuff = [[buffer.data[0][0], 0]]
	for i in range(buffer.rows):
		for j in range(buffer.cols):
			if(cbuff[-1][0] == buffer.data[i][j]):
				cbuff[-1][1] += 1
			else:
				cbuff.append([buffer.data[i][j], 1])
	return Buffer(cbuff, buffer.rows, buffer.cols, buffer.lx, buffer.hx, buffer.ly, buffer.hy, True)

def decompressBuffer(buffer):
	assert buffer.compressed == True, "Buffer is not compressed"
	nbuff = [[0] * buffer.cols for _ in range(buffer.rows)]
	pos = 0
	ctr = 0
	for i in range(buffer.rows):
		for j in range(buffer.cols):
			nbuff[i][j] = buffer.data[pos][0]
			ctr += 1
			if(ctr == buffer.data[pos][1]):
				pos += 1
				ctr = 0
	return Buffer(nbuff, buffer.rows, buffer.cols, buffer.lx, buffer.hx, buffer.ly, buffer.hy, False)

if __name__ == "__main__":
	func = lambda x, y: (0.2 * y - np.sin(x)) * (0.4 * y - np.cos(x))
	st = time.time()
	buff = getBuffer(100, 100, -5, 5, -5, 5, func)
	print(time.time() - st)
	printBuffer(buff)
