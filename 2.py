import functools
import itertools
import typing
import operator


def check_safety(it: typing.Iterable, negative: typing.Optional[bool] = None) -> bool:
    try:
        current = next(it)
    except StopIteration:
        return True  # reached end of iteration without encountering a safety violation

    if negative is None:
        negative = current < 0

    if negative and not current < 0 or not negative and not current > 0:
        return False  # current's sign does not match previous' sign
    elif not (1 <= abs(current) <= 3):
        return False  # delta from previous not within [1, 3]
    else:
        return check_safety(it, negative)


def check_safety_with_dampener(it: typing.Iterable, negative: typing.Optional[bool] = None, dampener: bool = True) -> bool:
    try:
        current = next(it)
    except StopIteration:
        return True  # reached end of iteration without encountering a safety violation

    if negative is None:
        set_negative = True
        negative = current < 0
    else:
        set_negative = False

    sign_mismatch = negative and not current < 0 or not negative and not current > 0
    delta_not_ok = not (1 <= abs(current) <= 3)
    if sign_mismatch or delta_not_ok:
        if dampener:
            if not set_negative:  # This is the first value in line, will not appear in next
                try:
                    next(it)  # skip the next value
                except StopIteration:
                    pass
            dampener = False  # unsafe value, but dampener was active. Disable it.
        else:  # Current value is unsafe, and dampener was already used
            return False
    return check_safety_with_dampener(it, negative, dampener)


def check_safety_new(row: typing.List[int]) -> bool:
    deltas = list(itertools.starmap(operator.sub, itertools.pairwise(row)))

    is_negative = list(map(lambda x: x < 0, deltas))
    signs_match = all(is_negative) or all(map(lambda x: not x, is_negative))
    deltas_ok = all(map(lambda x: 1 <= abs(x) <= 3, deltas))
    return signs_match and deltas_ok


def check_safety_dampener_new(row: typing.List[int]) -> bool:
    def exclude(l: typing.List, index: int) -> typing.List:
        """
        Return copy of list without element at index
        :param l:
        :param index:
        :return:
        """
        if not 0 <= index < len(l):
            raise ValueError(f'Index {index} out of bounds for list of length {len(l)}')
        return l[:index] + l[index + 1:]

    def outlier(key: bool, it: iter) -> typing.Optional[typing.Tuple[bool, int]]:
        group = list(it)
        return group[0] if len(group) == 1 else None

    def detect_potential_outliers(fn: typing.Callable[[int], bool], it: typing.Iterable) -> typing.Optional[typing.Tuple[int, int]]:
        matches = list(enumerate(map(fn, it)))
        matches.sort(key=operator.itemgetter(1))
        gs = itertools.groupby(matches, key=operator.itemgetter(1))
        os = list(filter(lambda x: x is not None, itertools.starmap(outlier, gs)))
        if len(os) == 1:
            index = os[0][0]
            return index, index + 1
        else:
            return None

    if check_safety_new(row):
        return True

    deltas = list(itertools.starmap(operator.sub, itertools.pairwise(row)))
    neg_outliers = detect_potential_outliers(lambda x: x < 0, deltas)
    delta_outliers = detect_potential_outliers(lambda x: 1 <= abs(x) <= 3, deltas)
    # really only care in case where there's a single outlier
    # If there are two distinct, then dampening won't work.
    # If there are two that are the same, then neg_outliers == delta_outliers and examining only neg_outliers is fine
    outliers = neg_outliers or delta_outliers
    if outliers:
        # See if removing eiter of the two elements that caused the outlier delta will pass safety check
        return check_safety_new(exclude(row, outliers[0])) or check_safety_new(exclude(row, outliers[1]))
    else:
        return False


def part_one(lines: typing.Iterable[typing.List[int]]) -> int:
    safe_line_new = map(lambda line:
                        check_safety(map(lambda x, y: x - y, line[1:], line[:-1])),
                        lines)
    return sum(map(int, safe_line_new))


def part_two(lines: typing.List[typing.List[int]]) -> int:
    safe_line_new = map(lambda line:
                        check_safety_with_dampener(map(lambda x, y: x - y, line[1:], line[:-1])),
                        lines)
    return sum(map(int, safe_line_new))


def main():
    with open('2_input.txt', 'r') as f:
        lines = list(map(lambda x: list(map(int, x.strip('\n').split(' '))), f.readlines()))
    print(part_one(lines))
    print(sum(map(int, map(check_safety_new, lines))))
    print(sum(map(int, map(check_safety_dampener_new, lines))))
    # print(part_two(lines))


if __name__ == '__main__':
    main()
