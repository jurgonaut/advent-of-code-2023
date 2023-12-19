import argparse
from copy import deepcopy

def get_result(map2D, height, width):
    result = 0
    stones = 0
    multiplier = 1
    for h in range(height-1, -1, -1):
        for w in range(width):
            if map2D[h][w] == "O":
                stones += 1
        result += stones * multiplier
        multiplier += 1
        stones = 0
    return result

def process_line(map2D, start_y, start_x, direction = []):
    height, width = len(map2D)-1, len(map2D[0])-1

    curr_y, curr_x = start_y, start_x
    stop_y = height if direction[0] == -1 else start_y
    stop_x = width if direction[1] == -1 else start_x

    while (curr_y >= 0 and curr_y <= height) and \
          (curr_x >= 0 and curr_x <= width):

        if map2D[curr_y][curr_x] == "O":
            tmp = map2D[curr_y][curr_x]
            map2D[curr_y][curr_x] = map2D[stop_y][stop_x]
            map2D[stop_y][stop_x] = tmp
            stop_y += direction[0]
            stop_x += direction[1]
        elif map2D[curr_y][curr_x] == "#":
            stop_y = curr_y + direction[0]
            stop_x = curr_x + direction[1]

        curr_y += direction[0]
        curr_x += direction[1]


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

    # Solver part 1
    if args.first:
        map2D_first = deepcopy(map2D)
        for i in range(width):
            process_line(map2D_first, 0, i, [1, 0])

        result = get_result(map2D_first, height, width)
        print(f"Result part 1: {result}")

    # Solve part 2
    if args.second:
        map2D_second = deepcopy(map2D)

        for i in range(1000):
            for i in range(width):
                process_line(map2D_second, 0, i, [1, 0])
            for i in range(height):
                process_line(map2D_second, i, 0, [0, 1])
            for i in range(width):
                process_line(map2D_second, height-1, i, [-1, 0])
            for i in range(height):
                process_line(map2D_second, i, width-1, [0, -1])

        result = get_result(map2D_second, height, width)
        print(f"Result part 2: {result}")