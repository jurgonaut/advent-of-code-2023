import argparse
from copy import deepcopy
from pprint import pprint
from PIL import Image
import numpy as np

def flood(unseen, seen, non_energized):
    point = unseen.pop()
    y, x = point[0], point[1]

    if (y, x) in seen:
        return
    seen.append((y, x))

    if map2D[y][x] == "#":
        return
    
    if map2D[y][x] == ".":
        non_energized.append((y, x))

    for d in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        dy, dx = y, x
        dy += d[0]
        dx += d[1]

        if dy >= height or dy < 0 or dx >= width or dx < 0:
            continue
        unseen.append((dy, dx))

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="path to input file")
    parser.add_argument(
        "--first", help="first half solution", action="store_true")
    parser.add_argument(
        "--second", help="second half solution", action="store_true")
    parser.add_argument(
        "--img", help="save map as image", action="store_true")
    args = parser.parse_args()

    # Parse input to 2D map
    dig_plan = []
    with open(args.input) as file:
        for line in file:
           l = line.strip()
           dig_plan.append(l.split())

    if args.first:
        print("Planing")
        min_y, max_y, y, min_x, max_x, x = 0,0,0,0,0,0
        for d in dig_plan:
            direction = d[0]
            distance = int(d[1])
            x = x + distance if direction == "R" else x
            x = x - distance if direction == "L" else x
            y = y + distance if direction == "D" else y
            y = y - distance if direction == "U" else y

            max_x = x if x > max_x else max_x
            min_x = x if x < min_x else min_x
            max_y = y if y > max_y else max_y
            min_y = y if y < min_y else min_y

        print(f"min and max {min_y}, {max_y} | {min_x}, {max_x}")

        height, width = abs(min_y) + abs(max_y), abs(min_x) + abs(max_x)
        print(f"height {height}, width {width}")
        map2D = [["." for i in range(width+1)] for j in range(height+1)]

        # We need to take into account that we could move into the -y/-x
        # relative from the start position, eg: first command is L ...
        y = abs(min_y) if max_y != 0 else abs(min_y) - abs(max_y)
        x = abs(min_x) if max_x != 0 else abs(min_x) - abs(max_x)
        print(f"start y {y} start x {x}")
        
        print("Digging")
        for d in dig_plan:
            direction = d[0]
            distance = int(d[1])
            for i in range(distance):
                x = x + 1 if direction == "R" else x
                x = x - 1 if direction == "L" else x
                y = y + 1 if direction == "D" else y
                y = y - 1 if direction == "U" else y
                map2D[y][x] = "#"

        print("Flooding")
        seen, unseen, non_energized = [], [], []

        # Start from edges
        unseen.extend([(h, 0) for h in range(height+1)])
        unseen.extend([(h, width) for h in range(height+1)])
        unseen.extend([(0, w) for w in range(width+1)])
        unseen.extend([(height, w) for w in range(width+1)])

        while unseen:
           flood(unseen, seen, non_energized)

        result = (len(map2D) * len(map2D[0])) - len(non_energized)
        print(f"Result part 1: {result}")

        if args.img:
            for ne in non_energized:
                map2D[ne[0]][ne[1]] = "O"
            write_image(map2D, "map-flooded")

    if args.second:
        pass