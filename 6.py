import itertools
from typing import Tuple, List, Set


def main():
    with open('6_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    print(len(lines))
    def enum_line(i: int, line: str): return map(lambda enum: (i, *enum), enumerate(line))
    line_enums = itertools.starmap(enum_line, enumerate(lines))
    s = sorted(itertools.chain(*line_enums), key=lambda x: x[2])
    def is_start(x: Tuple[int, int, str]) -> Tuple[int, int]: return x[2] == '^'
    def is_obstacle(x: Tuple[int, int, str]) -> Tuple[int, int]: return x[2] == '#'
    def get_pos(x: Tuple[int, int, str]) -> Tuple[int, int]: return (x[0], x[1])
    start = next(map(get_pos, filter(is_start, s)))
    obstacles = list(map(get_pos, filter(is_obstacle, s)))

    direction = (0, 1)
    visited = set()
    pos = tuple(start)
    while True:
        if (direction[0] == 0 and direction[1] == 0) or (direction[0] != 0 and direction[1] != 0):
            raise ValueError("Invalid direction, expected a cardinal direction, got: " + str(direction))
        visited.add(pos)
        next_pos = pos[0] + direction[0], pos[1] + direction[1]
        try:
            lines[next_pos[0]][next_pos[1]]
        except IndexError:
            break
        if next_pos in obstacles:  # change direction
            next_pos = pos  # can't be in an obstacle, so back up
            direction = direction[1], direction[0] * -1
        pos = next_pos

    print(len(visited))  # 4646 is too low


if __name__ == '__main__':
    main()
