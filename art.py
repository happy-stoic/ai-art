"""
Todo:
- Draw something using aggdraw
- Parameterize the drawing
- Randomly manipulate the parameters
- Change the parameters using scikit-learn
- Implement a simple recommender system script
- Try it out with different source images, stop when something looks cool enough.
"""

import aggdraw as ad
import sklearn as sk
from PIL import Image
import numpy as np

# draw something simple
def test_graphics2():
    from aggdraw import Draw, Symbol, Pen
    symbol = Symbol("M400 200 L400 400")
    pen = Pen("red")
    image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
    canvas = Draw(image)
    canvas.symbol((0, 0), symbol, pen)
    canvas.flush()
    image.show()

test_graphics2()