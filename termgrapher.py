from term_backend import termGrapher

_tg_backend = termGrapher()

def new(rows, cols, lx, hx, ly, hy, data=None):
    return _tg_backend.new(rows=rows, cols=cols, lx=lx, hx=hx, ly=ly, hy=hy, data=data)

def get():
    return _tg_backend.get()

def set(figure):
    _tg_backend.set(figure)

def clear(figure=None):
    _tg_backend.clear(figure=figure)

def graph(comparator, figure=None):
    _tg_backend.graph(comparator=comparator, figure=figure)

def plot(x, y, figure=None):
    _tg_backend.plot(x=x, y=y, figure=figure)

def scatter(x, y, figure=None):
    _tg_backend.scatter(x=x, y=y, figure=figure)

def show(figure=None):
    _tg_backend.show(figure=figure)

def save(filename="figure", figure=None):
    _tg_backend.save(filename=filename, figure=figure)

def load(path):
    return _tg_backend.load(path=path)
