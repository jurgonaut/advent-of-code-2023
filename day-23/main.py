import argparse
from pprint import pprint
from copy import deepcopy
from PIL import Image
import numpy as np

def write_image(map2D, name):
    pixels = []

    for h in range(len(map2D)):
        l = []
        for w in range(len(map2D[0])):
            if map2D[h][w] == "#":
                l.append((0, 0, 0))
            elif map2D[h][w] == "O":
                l.append((51, 51, 255))
            else:
                l.append((255, 255, 255))
        pixels.append(l)

    # Convert the pixels into an array using numpy
    array = np.array(pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save(f'{name}.png')

def move_part_1(path):
    next_positions = []
    last_move = path[-1]
    y, x = last_move[0], last_move[1],

    for d in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        dy, dx = y, x
        dy += d[0]
        dx += d[1]

        # if out of bounds, seen or wall continue
        if (dy >= height or dy < 0 or dx >= width or dx < 0) or \
           ((dy, dx) in path) or \
           (map2D[dy][dx] == "#"):
            continue

        # if empty or going down slope, add to queue
        if map2D[dy][dx] == "." or \
           d == [1,0] and map2D[dy][dx] == "v" or \
           d == [0,1] and map2D[dy][dx] == ">":
            next_positions.append((dy, dx))

    return next_positions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="path to input file")
    parser.add_argument(
        "--first", help="first half solution", action="store_true")
    parser.add_argument(
        "--second", help="second half solution", action="store_true")
    args = parser.parse_args()

    # Parse input into list
    map2D = []
    with open(args.input) as file:
        for line in file:
           l = []
           for c in line.strip():
               l.append(c)
           map2D.append(l)

    height, width = len(map2D), len(map2D[0])

    start_y, start_x = 0, 1

    # Solve part 1
    if args.first:
        paths = [[(start_y, start_x, 0)]]
        completed_paths = []

        while True:
            if not paths:
                break

            tmp_paths = []
            for p in paths:
                next = move_part_1(p)

                if not next:
                    completed_paths.append(p)
                    continue

                if len(next) == 1:
                    p.append(next[0])
                    tmp_paths.append(p)
                    continue

                for n in next:
                    new_path = deepcopy(p)
                    new_path.append(n)
                    tmp_paths.append(new_path)

            paths = tmp_paths

        max_steps = 0
        for p in completed_paths:
            if len(p) > max_steps:
                max_steps = len(p)

        print(f"Result part 1: {max_steps-1}")

    # Solve part 2
    if args.second:
        pass