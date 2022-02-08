# PyTerm-Grapher  
## Sai Akarsh (12-12-21)  

### Description  
A graphing tool which prints in ASCII on the terminal.  
This is a test project with a goal of replicating the `matplotlib.pyplot` library's basic utilities.  

### How to use  
Here is a sample code snippet,  
```python
import numpy as np
import termgrapher as tg

# scatter plot
tg.scatter([1, 2, 3], [5, 2, 4])
tg.show()

# plot
fig = tg.new(50, 100, -5, 5, 0, 25)
x = np.linspace(-5, 5, 10)
tg.plot(x, x**2)
tg.show(fig)

# function plot
tg.new(100, 100, -10, 10, -10, 10)
tg.graph(lambda x, y: y)
tg.graph(lambda x, y: 0.2 * y - np.sin(x))
tg.show()
```  

You can also run the `demo.py` file to understand the basic functions available.  

### Features  
- Make a canvas with custom size and range. If you don't create an canvas, then it will use the default canvas. When you create a canvas, it will replace the default with the newly created canvas.  
- Plotting simple 2D graph based on two input arrays x, y.  
- Scatter plot points using two input arrays x, y.  
- Function plot is a new idea. You can plot the function directly rather than precalulating the points and plotting them instead. Function plot does not work as mentioned earlier but used a concept from shaders in Graphics. We calculate the color of each pixel/coordinate using the function output on that coordinate. This is done very efficiently using the magic of numpy.  
- You can print the canvas on the terminal and also save the canvas in a file and load it later on. It uses a simple compression and decompression technique in order to store the canvas in a file to reduce redudancy and save disk space.  