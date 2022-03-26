"""
Todo:
- Change the parameters using scikit-learn
- Implement a simple recommender system script
- Try it out with different source images, stop when something looks cool enough.
"""

from aggdraw import Draw, Symbol, Pen, Brush
import sklearn as sk
from PIL import Image
import numpy as np
import random
from random import random, choice


# Set up an image.
image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
canvas = Draw(image)


def add_a_mark_to_the_canvas(canvas, symbol_params, pen, start_point):
    """Add a symbol to the canvas using a brush or pen."""
    # Turn the parameters into a command.
    symbol = Symbol(" ".join(symbol_params))
    # Add the mark to the canvas.
    canvas.symbol(start_point, symbol, pen)
    canvas.flush()


def gen_symbol_params():
    letters = "MLHVCSQTZ"
    params = []

    scale = random()*1000
    n_strokes = int(random()*20)

    # A random number generator.
    rand = lambda : random()*scale

    # Create a string of commands for this symbol.
    for _ in range(n_strokes):
        params.append(f"{choice(letters)}{rand()}")
        params.append(str(rand()))
    return params


def get_mark_maker_params():
    r_colour = lambda : int(random()*255)
    color = (r_colour(), r_colour(), r_colour())
    params = dict(
        color = color,
        opacity = int(155 + random()*100)
    )
    return params


def get_pen_params():
    params = get_mark_maker_params()
    params["width"] = int(random()*10)
    return params


def generate_a_mark_maker():
    """Define a pen or brush to add a symbol."""
    use_pen = random() > 0.5
    if use_pen:
        return Pen(**get_pen_params())
    else:
        return Brush(**get_mark_maker_params())


def gen_start_point():
    return ((random()*400, random()*400))


for i_mark in range(1000):
    symbol_params = gen_symbol_params()
    start_point = gen_start_point()
    mark_maker = generate_a_mark_maker()
    add_a_mark_to_the_canvas(canvas, symbol_params, mark_maker, start_point)

image.show()