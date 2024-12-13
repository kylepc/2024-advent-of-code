from typing import List


def is_valid(test: int, numbers: List[int], cat: bool = False) -> bool:
    if len(numbers) == 1:
        return test == numbers[0]
    elif is_valid(test, [numbers[0] + numbers[1]] + numbers[2:], cat):
        return True
    elif is_valid(test, [numbers[0] * numbers[1]] + numbers[2:], cat):
        return True
    elif cat and is_valid(test, [int(str(numbers[0]) + str(numbers[1]))] + numbers[2:], cat):
        return True
    else:
        return False


def part_1(equations):
    result = 0
    for eq in equations:
        test = eq[0]
        numbers = eq[1]
        if is_valid(test, numbers, False):
            result += test
    return result


def part_2(equations):
    return sum(map(lambda eq: eq[0] if is_valid(eq[0], eq[1], True) else 0, equations))


def main():
    with open('7_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    split_lines = [line.split(': ') for line in lines]
    equations = [(int(x[0]), list(map(int, x[1].split(' ')))) for x in split_lines]
    assert len(lines) == len(equations)

    print(part_1(equations))
    print(part_2(equations))


if __name__ == '__main__':
    main()