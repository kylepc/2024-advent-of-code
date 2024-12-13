from typing import List


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
    for eq in equations:
        test = eq[0]
        numbers = eq[1]
        if is_valid(test, numbers):
            result += test

    print(result)


if __name__ == '__main__':
    main()