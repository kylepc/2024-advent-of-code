import itertools
import operator
from typing import List, Iterable, Any, Callable

target = 'XMAS'


def part_one(data: List[str]) -> int:
    def len_pred(x): return len(x) == len(target)
    def match_pred(x): return all(itertools.starmap(operator.eq, zip(x, target, strict=True)))

    def walk_over(start: int, length: int, direction: Callable[[int, int], int]) -> Callable[[Iterable], Any]:
        position = start

        def fn(it: Iterable) -> Any:
            nonlocal position, start, length
            if position == direction(start, length):
                raise StopIteration()
            elif position < 0:
                return ''
            else:
                n = itertools.islice(it, position, position + 1)
                position = direction(position, 1)
                return next(n)

        return fn


    count = 0
    for i, row in enumerate(data):
        for j, _ in enumerate(row):
            forward = row[j:j + len(target)]
            down = list(map(lambda x: x[j], data[i:i + len(target)]))
            diag_right = list(map(walk_over(j, len(target), operator.add), data[i: i + len(target)]))
            diag_left = list(map(walk_over(j, len(target), operator.sub), data[i: i + len(target)]))
            to_check_forward = [forward, down, diag_left, diag_right]
            to_check_reverse = map(lambda x: x[::-1], to_check_forward)
            to_check = itertools.chain(to_check_forward, to_check_reverse)
            count += sum(map(int, map(match_pred, filter(len_pred, to_check))))

    return count


def main():
    with open('4_input.txt', 'r') as f:
        data = [line.strip('\n') for line in f.readlines()]
    print(part_one(data))


if __name__ == '__main__':
    main()
