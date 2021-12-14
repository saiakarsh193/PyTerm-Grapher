import numpy as np
import termgrapher as tg

# graphing
tg.new(100, 100, -10, 10, -10, 10)
tg.graph(lambda x, y: y)
tg.graph(lambda x, y: 0.2 * y - np.sin(x))
tg.show()

# plot
fig = tg.new(50, 100, -5, 5, 0, 25)
x = np.linspace(-5, 5, 10)
tg.plot(x, x**2)
tg.show(fig)

# scatter
fig = tg.new(50, 50, -10, 10, -10, 10)
tg.scatter([1, 2, 3], [5, 2, 4])
tg.show(fig)