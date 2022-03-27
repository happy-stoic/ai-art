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
import pandas as pd
from random import random, choice
import pickle


MAXIMUM_STROKE_SIZE = 500
MAXIMUM_CURVE_PARTS = 6
MAXIMUM_START_POINT = 400
MAXIMUM_PEN_WIDTH = 40
N_MARKS = 6


def add_a_mark_to_the_canvas(canvas, symbol_params, pen, start_point):
    """Add a symbol to the canvas using a brush or pen."""
    # Turn the parameters into a command.
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
        mark_spec = (color, opacity, width)
        return Pen(*mark_spec), mark_spec
    else:
        mark_spec = (color, opacity, None)
        return Brush(*mark_spec[:2]), mark_spec


def gen_random_marks():
    # Generate the symbols that will decorate the canvas (random pen and brushstrokes).
    gen_stroke_size = lambda : random()*MAXIMUM_STROKE_SIZE

    # Create all the brushstroke paths; randomly.
    start_points = []
    marks = []
    stroke_lengths = (np.random.random(N_MARKS)*MAXIMUM_STROKE_SIZE).astype(int)
    for length in stroke_lengths:
        start_point = ((random()*MAXIMUM_START_POINT,
                        random()*MAXIMUM_START_POINT))
        valid_letters = "MLHVCSQTZ"
        letters = [choice(valid_letters) for x in range(length)]
        sizes = [gen_stroke_size() for x in range(length)]
        movements = [gen_stroke_size() for x in range(length)]
        mark = gen_sentence_of_strokes(letters, sizes, movements)
        start_points.append(start_point)
        marks.append(mark)
    
    return start_points, marks 


def gen_random_mark_makers():
    # Create all the pens and brushes randomly, and record the variables we used for them.
    mark_makers = []
    mark_specs = []
    for _ in range(N_MARKS):
        mm, ms = get_mark_maker()
        mark_makers.append(mm)
        mark_specs.append(ms)
    return mark_makers, mark_specs


if __name__ == "__main__":

    # Set up a canvas to paint on.
    image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
    canvas = Draw(image)

    # Add Symbols with Pens and Brushes; paint that picture!
    start_points, marks = gen_random_marks()
    mark_makers, mark_specs = gen_random_mark_makers()
    for start_point, mark, mark_maker in zip(start_points, marks, mark_makers):
        print(mark)
        add_a_mark_to_the_canvas(canvas, mark, mark_maker, start_point)
    
    # Save the image.
    now = datetime.now()
    filename = f"data/art_{now.strftime('%Y_%m_%d_%H_%M_%S')}"
    image.save(filename + ".png")

    print("DATA 1")
    print(marks)
    print(mark_specs)
    print(start_points)

    # Save instructions for how to re-create the image in a DataFrame.
    df = pd.DataFrame()
    df['start_points'] = start_points
    df['marks'] = marks
    df['mark_specs'] = mark_specs

    # Save it.
    df.to_pickle(filename + '.pickle')

    # Recreate the image and check it looks the same.
    # Load description.
    df2 = pickle.load(open(filename + '.pickle', 'rb'))
    # Set up a blank canvas.
    image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
    canvas = Draw(image)
    # Re-create the markmaker for the mark, then apply saved params.
    start_points = df2['start_points'].values
    marks = df2['marks'].values
    mark_specs = df2['mark_specs'].values

    print("DATA 2")
    print(marks)
    print(mark_specs)
    print(start_points)

    for start_point, mark, mark_spec in zip(start_points, marks, mark_specs):
        # Re-create a pen or a brush.
        if mark_spec[2]:
            mark_maker = Pen(*mark_spec)
        else:
            mark_maker = Brush(*mark_spec[:2])
        # Re-create the symbol
        add_a_mark_to_the_canvas(canvas, mark, mark_maker, start_point)

    # Save the second image.
    now = datetime.now()
    filename = f"data/art_{now.strftime('%Y_%m_%d_%H_%M_%S_recreated')}"
    image.save(filename + ".png")