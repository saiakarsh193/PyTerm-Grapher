import math
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
	umap = lambda n, il, ih, fl, fh: fl + ((n - il) / (ih - il)) * (fh - fl)
	sign = lambda val: 1 if(val >= 0) else -1
	edgeval = lambda v1, v2, v3, v4: int(bool(abs(v1 + v2 + v3 + v4) != 4))
	precomp = [[0] * (cols + 1) for _ in range(rows + 1)]
	buffer = [[0] * cols for _ in range(rows)]
	for i in range(rows + 1):
		for j in range(cols + 1):
			precomp[i][j] = sign(comp(umap(j, 0, cols, lx, hx), umap(i, 0, rows, hy, ly)))
	for i in range(rows):
		for j in range(cols):
			buffer[i][j] = edgeval(precomp[i][j], precomp[i + 1][j], precomp[i + 1][j + 1], precomp[i][j + 1])
	return Buffer(buffer, rows, cols, lx, hx, ly, hy)

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
	func = lambda x, y: (0.2 * y - math.sin(x)) * (0.4 * y - math.cos(x))
	st = time.time()
	buff = getBuffer(100, 100, -5, 5, -5, 5, func)
	print(time.time() - st)
	printBuffer(buff)
	cbuff = compressBuffer(buff)
	nbuff = decompressBuffer(cbuff)
	printBuffer(nbuff)
	print("Compression ratio: {0:.3f}".format(nbuff.size() / cbuff.size()))