import typing


def part_one(left: typing.List[int], right: typing.List[int]) -> int:
    merged = zip(left, right)
    distance = map(lambda x: abs(x[0] - x[1]), merged)
    return sum(distance)


def part_two(left: typing.List[int], right: typing.List[int]) -> int:
    score = 0
    for l in left:
        # Note: could be made more efficient by leveraging fact that left and right are sorted
        count = sum(map(lambda r: 1, filter(lambda r: r == l, right)))
        score += l * count
    return score


def main():
    with open('1_input.tsv', 'r') as f:
        lines = list(map(lambda x: x.strip('\n').split('   '), f.readlines()))
    left = sorted(map(lambda x: int(x[0]), lines))
    right = sorted(map(lambda x: int(x[1]), lines))
    print(part_one(left, right))
    print(part_two(left, right))


if __name__ == '__main__':
    main()
