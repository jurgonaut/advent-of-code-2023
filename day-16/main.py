import argparse
from copy import deepcopy
from pprint import pprint

def explore(beams, map2D, explored):
    height, width = len(map2D)-1, len(map2D[0])-1
    # Get beam and do some prerequisite checks
    b = beams.pop()

    if b in explored:
        return []
    explored.add(b)

    char = map2D[b[0]][b[1]]

    # Transform direction based on type of mirror we encountered
    if char == "|" and b[3] != 0:
        next_beams = [
            (b[0], b[1], 1, 0),
            (b[0], b[1], -1, 0)
        ]
    elif char == "-" and b[2] != 0:
        next_beams = [
            (b[0], b[1], 0, 1),
            (b[0], b[1], 0, -1)
        ]
    elif char == "/":
        next_beams = [(b[0], b[1], b[3] * -1, b[2] * -1)]
    elif char == "\\":
        next_beams = [(b[0], b[1], b[3], b[2])]
    else:
        next_beams = [b]

    # Move the new beam and add it to the yet to be explored beams if 
    # it's not out of bounds
    for nb in next_beams:
        moved_nb = (nb[0] + nb[2], nb[1] + nb[3], nb[2], nb[3])
        if (moved_nb[0] < 0 or moved_nb[0] > height) or \
           (moved_nb[1] < 0 or moved_nb[1] > width):
            continue

        beams.append(moved_nb)

    return next_beams

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="path to input file")
    parser.add_argument(
        "--first", help="first half solution", action="store_true")
    parser.add_argument(
        "--second", help="second half solution", action="store_true")
    args = parser.parse_args()

    # Parse input to 2D map
    map2D = []
    with open(args.input) as file:
        for line in file:
           l = []
           for c in line.strip():
               l.append(c)
           map2D.append(l)

    if args.first:
        map2D_first = deepcopy(map2D)

        beam = (
            0,  # 0 = y 
            0,  # 1 = x 
            0,  # 2 = y move direction
            1   # 3 = x move direction
        )
        explored = set()
        beams = [beam]
        
        while beams:
            next_beams = explore(beams, map2D_first, explored)

            for nb in next_beams:
                if map2D[nb[0]][nb[1]] == ".":
                    map2D[nb[0]][nb[1]] = "#"

        # Get new set with only y and x values (this removes duplicates)
        pruned = set([(e[0], e[1]) for e in explored])
        print(f"Result part 1: {len(pruned)}")

    if args.second:
        map2D_second = deepcopy(map2D)
        height, width = len(map2D_second), len(map2D_second[0])
        max = 0
        beams_directions = []
        
        # Add a starting beam for all directions to a list
        for w in range(width):
            beams_directions.extend([(0, w, 1, 0), (height-1, w, -1, 0)])
        for h in range(height):
            beams_directions.extend([(h, 0, 0, 1), (h, width-1, 0, -1)])

        # Loop trough all the starting beams and do the same as part 1
        for beam in beams_directions:
            explored = set()
            beams = [beam]
            while beams:
                next_beams = explore(beams, map2D_second, explored)
        
            pruned = set([(e[0], e[1]) for e in explored])

            if len(pruned) > max:
                max = len(pruned)

        print(f"Result part 2: {max}")
