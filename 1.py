import timeit
import typing


def part_one(left: typing.List[int], right: typing.List[int]) -> int:
    merged = zip(left, right)
    distance = map(lambda x: abs(x[0] - x[1]), merged)
    return sum(distance)


def part_two_faster(left: typing.List[int], right: typing.List[int]) -> int:
    r_count: typing.Dict[int, int] = {}
    for r in right:
        if r in r_count:
            r_count[r] += 1
        else:
            r_count[r] = 1

    return sum(map(lambda l: l * r_count.get(l, 0), left))


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
    print(part_two_faster(left, right))

    # original took 5.3 seconds, faster took 0.01 seconds
    # print(f'original: {timeit.timeit(lambda: part_two(left, right), globals=globals(), number=100)}')
    # print(f'faster: {timeit.timeit(lambda: part_two_faster(left, right), globals=globals(), number=100)}')


if __name__ == '__main__':
    main()
