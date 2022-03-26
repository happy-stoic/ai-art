"""
Todo:
- Make as many parameters as possible continuous
- Add as many parameters as possible
- Change the parameters using scikit-learn
- Implement a simple recommender system script
- Try it out with different source images, stop when something looks cool enough.
"""

from turtle import color
from aggdraw import Draw, Symbol, Pen, Brush
import sklearn as sk
from PIL import Image
import numpy as np
import random


"""
Docs: 

Parameters path (str) – An SVG-style path descriptor.
The following operators are supported: 
M (move), L (line), H (horizontal line), V (vertical line), C (cubic bezier),
S (smooth cubic bezier), Q (quadratic bezier), T (smooth quadratic bezier),
 and Z (close path).
Use lower-case operators for relative coordinates, upper-case for absolute coordinates.

aggdraw.Pen() Creates a Pen object.
Parameters
• color (tuple or str or int) – Pen color. This can be a color tuple (R, G, B) or (R, G, B, A), a CSS-style color name, or a color integer (0xaarrggbb).
• width (int, optional) – Pen width. Default 1.
• opacity (int, optional) – Pen opacity. Default 255.
• linejoin (int, optional) – Type of line_join. Types are 0=miter_join 1=miter_join_revert; 2=round_join; 3=bevel_join; 4=miter_join_round. Default 0 (miter join).
• linecap (int, optional) – Type of linecap. Types are 0=butt_cap; 1=square_cap; 2=round_cap. Default 1 (butt cap).
• miterlimit (float, optional) – Type of miterlimit. Default 4.0.

aggdraw.Brush() Creates a brush object.
Parameters
• color (tuple or str or int) – Brush color. This can be a color tuple (R, G, B) or (R, G, B, A), a CSS-style color name, or a color integer (0xaarrggbb).
• opacity (int, optional) – Brush opacity. Default 255.
"""

# Set up an image.
image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
canvas = Draw(image)

def add_a_mark_to_the_canvas(canvas, symbol_params, pen_params, start_point):
    """Add a symbol to the canvas using a brush or pen."""
    # Turn the parameters into a command.
    symbol = Symbol(" ".join(symbol_params))
    pen = Pen(" ".join(pen_params))
    # Add the mark to the canvas.
    canvas.symbol(start_point, symbol, pen)
    canvas.flush()


def gen_symbol_params(scale=400, len=12):
    letters = "MLHVCSQTZ"
    params = []
    # A random number generator.
    rand = lambda : random.random()*scale 

    # Create a string of commands for this symbol.
    for _ in range(len):
        params.append(f"{random.choice(letters)}{rand()}")
        params.append(str(rand()))
    return params


def gen_pen_params():
    colours = ["blue", "red", "green"]
    return [random.choice(colours)]


for i_mark in range(10):
    symbol_params = gen_symbol_params()
    pen_params = gen_pen_params()
    print(symbol_params)
    print(pen_params)
    start_point = ((random.random()*400, random.random()*400))
    add_a_mark_to_the_canvas(canvas, symbol_params, pen_params, start_point)


image.show()