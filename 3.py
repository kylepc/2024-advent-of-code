import functools
import itertools
import operator
import re
from typing import List


number = r'[0-9]{1,3}'
mul_regex = re.compile(rf'mul\(({number},{number})\)')


def part_one(data: str) -> int:
    fn_calls: List[str] = mul_regex.findall(data)
    int_pairs: List[List[int, int]] = map(lambda x:
                                          map(lambda y: int(y), x.split(',')),
                                          fn_calls)
    products: List[int] = itertools.starmap(lambda w, z: w * z, int_pairs)
    return sum(products)


def part_two(data: str) -> int:
    active = True
    i = 0
    total = 0
    while i < len(data):
        if active and data[i:].startswith('mul'):
            inc = len('mul')
            if match := mul_regex.match(data[i:]):
                inc += len(f'({match.group(1)})')
                total += functools.reduce(operator.mul, map(int, match.group(1).split(',')))
        elif data[i:].startswith('do()'):
            active = True
            inc = len('do()')
        elif data[i:].startswith('don\'t()'):
            active = False
            inc = len('don\'t()')
        else:
            inc = 1
        i += inc

    return total


def main():
    with open('3_input.txt', 'r') as f:
        data = f.read()

    print(part_one(data))
    print(part_two(data))


if __name__ == '__main__':
    main()
