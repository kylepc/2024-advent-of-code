import functools
import itertools
import operator
from typing import Callable, Tuple, List


def is_valid(test: int, numbers: List[int]) -> bool:
    if len(numbers) == 1:
        return test == numbers[0]
    elif is_valid(test, [numbers[0] + numbers[1]] + numbers[2:]):
        return True
    elif is_valid(test, [numbers[0] * numbers[1]] + numbers[2:]):
        return True
    else:
        return False


def main():
    with open('7_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    split_lines = [line.split(': ') for line in lines]
    equations = [(int(x[0]), list(map(int, x[1].split(' ')))) for x in split_lines]
    assert len(lines) == len(equations)

    result = 0
    result_new = 0
    for eq in equations:
        test = eq[0]
        numbers = eq[1]
        num_pairs = len(numbers) - 1
        # including len(paris) elements of each so that we get all possible permutations +++, ++*, ... ***
        # but is that necessary? Is there a smaller iterable I could pass to this function?
        # TODO: can't do this, takes way too long
        # op_permutations = list(itertools.permutations([operator.add] * num_pairs + [operator.mul] * num_pairs, num_pairs))
        #
        # def combiner(op_perm: List[Callable[[int, int], int]]) -> Callable[[int, int], int]:
        #     op_it = iter(op_perm)
        #
        #     def fn(a: int, b: int) -> int:
        #         op = next(op_it)
        #         return op(a, b)
        #     return fn
        #
        # for op_permutation in op_permutations:
        #     if functools.reduce(combiner(op_permutation), numbers) == test:
        #         result += test
        #         break

        if is_valid(test, numbers):
            result_new += test

    print(result)
    print(result_new)


if __name__ == '__main__':
    main()