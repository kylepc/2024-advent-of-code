import functools
import itertools
import operator
import re
from typing import List, Callable

number = r'[0-9]{1,3}'
mul_re = rf'mul\(({number},{number})\)'
do_re = r'do\(\)'
dont_re = r'don\'t\(\)'
mul_regex = re.compile(mul_re)


def part_one(data: str) -> int:
    fn_calls: List[str] = mul_regex.findall(data)
    int_pairs: List[List[int, int]] = map(lambda x:
                                          map(lambda y: int(y), x.split(',')),
                                          fn_calls)
    products: List[int] = itertools.starmap(lambda w, z: w * z, int_pairs)
    return sum(products)


def part_two_iter(data: str) -> int:
    def filter_closure(active: bool = True) -> Callable[[re.Match[str]], bool]:
        def fn(match: re.Match[str]) -> bool:
            nonlocal active
            if match.group(0).startswith('don\'t'):  # order matters, "don't" starts with "do"
                active = False
            elif match.group(0).startswith('do'):
                active = True
            return active and match.group(0).startswith('mul')
        return fn

    fn_regex = re.compile(f'({mul_re}|{do_re}|{dont_re})')
    fns = fn_regex.finditer(data)
    active_muls = filter(filter_closure(), fns)
    active_mul_inputs = map(lambda g: g.group(2), active_muls)
    int_pairs = map(lambda x: map(int, x.split(',')), active_mul_inputs)
    products = itertools.starmap(operator.mul, int_pairs)
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
    print(part_two_iter(data))


if __name__ == '__main__':
    main()
