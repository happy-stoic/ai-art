"""
Todo:
- Tidy up the parameters so that you can define a painting in one place
- Change the parameters using scikit-learn
- Implement a simple recommender system script
- Try it out with different source images, stop when something looks cool enough.
"""

from datetime import datetime
from aggdraw import Draw, Symbol, Pen, Brush
import sklearn as sk
from PIL import Image
import numpy as np
import random
from random import random, choice


MAXIMUM_STROKE_SIZE = 500
MAXIMUM_CURVE_PARTS = 100
MAXIMUM_START_POINT = 400
MAXIMUM_PEN_WIDTH = 10
N_MARKS = 100


def add_a_mark_to_the_canvas(canvas, symbol_params, pen, start_point):
    """Add a symbol to the canvas using a brush or pen."""
    # Turn the parameters into a command.
    print(f"FACTORY: {symbol_params}")
    symbol = Symbol(symbol_params)
    # Apply the symbol to the canvas.
    canvas.symbol(start_point, symbol, pen)
    canvas.flush()


def gen_stroke_part(letter, size, move):
    """Create a single stroke command."""
    return f"{letter}{size} {move}"


def gen_sentence_of_strokes(letters, sizes, movements):
    """Generate a sequence of strokes."""
    sentence = []
    for l, s, m in zip(letters, sizes, movements):
        sentence.append(gen_stroke_part(l,s,m))
    sentence = " ".join(sentence)
    print(f"STROKES: {sentence}")
    return sentence


def get_mark_maker():
    # Create all the Pens and Brushes; randomly.
    # Randomly select a brush or pen.
    use_pen = random() > 0.5
    # Generate a random colour.
    r_colour = lambda : int(random()*255)
    color = (r_colour(), r_colour(), r_colour())
    # Generate a random opacity.
    opacity = int(random()*255)
    # Generate a random width.
    width = int(random()*MAXIMUM_PEN_WIDTH)
    # Create a mark maker
    if use_pen:
        return Pen(color=color, opacity=opacity, width=width)
    else:
        return Brush(color=color, opacity=opacity)


if __name__ == "__main__":

    # Set up a canvas to paint on.
    image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
    canvas = Draw(image)

    # Generate the symbols that will decorate the canvas (random pen and brushstrokes).
    curve_parts = int(random()*MAXIMUM_CURVE_PARTS)
    stroke_sizes = lambda : random()*MAXIMUM_STROKE_SIZE
    start_points = ((random()*MAXIMUM_START_POINT, random()*MAXIMUM_START_POINT))

    # Create all the brushstroke paths; randomly.
    marks = []
    stroke_lengths = (np.random.random(N_MARKS)*MAXIMUM_STROKE_SIZE).astype(int)
    for length in stroke_lengths:
        valid_letters = "MLHVCSQTZ"
        letters = [choice(valid_letters) for x in range(length)]
        sizes = [stroke_sizes() for x in range(length)]
        movements = [stroke_sizes() for x in range(length)]
        mark = gen_sentence_of_strokes(letters, sizes, movements)
        marks.append(mark)

    # Create all the pens and brushes randomly.
    mark_makers = []
    for i_mm in range(N_MARKS):
        mark_makers.append(get_mark_maker())

    # Add Symbols with Pens and Brushes; paint that picture!
    for mark, mark_maker in zip(marks, mark_makers):
        add_a_mark_to_the_canvas(canvas, mark, mark_maker, start_points)
    
    # Save the image.
    now = datetime.now()
    image.save(f"data/art_{now.strftime('%Y_%m_%d_%H_%M_%S')}.png")

    # TODO: Save the params that I liked