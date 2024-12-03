import itertools
import re
from typing import List


def part_one(data: str) -> int:
    number = r'[0-9]{1,3}'
    mul_regex = re.compile(rf'mul\(({number},{number})\)')
    fn_calls: List[str] = mul_regex.findall(data)
    int_pairs: List[List[int, int]] = map(lambda x:
                                          map(lambda y: int(y), x.split(',')),
                                          fn_calls)
    products: List[int] = itertools.starmap(lambda w, z: w * z, int_pairs)
    return sum(products)


def part_two(data: str) -> int:
    return 0


def main():
    with open('3_input.txt', 'r') as f:
        data = f.read()

    print(part_one(data))
    print(part_two(data))


if __name__ == '__main__':
    main()
