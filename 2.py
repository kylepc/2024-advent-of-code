import itertools
import typing
import operator


def check_safety(row: typing.List[int]) -> bool:
    deltas = list(itertools.starmap(operator.sub, itertools.pairwise(row)))

    is_increasing = list(map(lambda x: x < 0, deltas))  # negative values indicate lhs < rhs; i.e. the values are increasing
    signs_match = all(is_increasing) or all(map(lambda x: not x, is_increasing))
    deltas_ok = all(map(lambda x: 1 <= abs(x) <= 3, deltas))
    return signs_match and deltas_ok


def check_safety_dampener(row: typing.List[int]) -> bool:
    def exclude(lst: typing.List, index: int) -> typing.List:
        """
        Return copy of list without element at index
        :param lst: a list of any type
        :param index: any integer [0, len(lst))
        :return: a list of the same type as l, with one less item
        """
        if not 0 <= index < len(lst):
            raise ValueError(f'Index {index} out of bounds for list of length {len(lst)}')
        return lst[:index] + lst[index + 1:]

    def outlier_index(key: bool, it: iter) -> typing.Optional[int]:
        group = list(it)
        # group is [(key, value), ...]
        return group[0][0] if len(group) == 1 else None  # if there are multiple values, they're not an outlier

    def detect_potential_outliers(fn: typing.Callable[[int], bool], it: typing.Iterable) -> typing.Optional[typing.Tuple[int, int]]:
        matches = list(enumerate(map(fn, it)))
        # sort on boolean result of fn; has form [(index, bool), ...]
        matches.sort(key=operator.itemgetter(1))
        groups = itertools.groupby(matches, key=operator.itemgetter(1))  # expects sorted input
        outlier_indices = list(filter(lambda x: x is not None, itertools.starmap(outlier_index, groups)))
        if len(outlier_indices) == 1:
            index = outlier_indices[0]
            return index, index + 1
        else:  # if more than one outlier index found, then dampening will not work
            return None

    if check_safety(row):
        return True  # row safe without dampening

    deltas = list(itertools.starmap(operator.sub, itertools.pairwise(row)))
    neg_outliers = detect_potential_outliers(lambda x: x < 0, deltas)
    delta_outliers = detect_potential_outliers(lambda x: 1 <= abs(x) <= 3, deltas)
    # If neg and delta outliers are both defined and distinct, then dampening won't work.
    # If they are the same, then neg_outliers == delta_outliers and examining only neg_outliers is fine
    outliers = neg_outliers or delta_outliers
    if outliers:
        # See if removing eiter of the two elements that caused the outlier delta will pass safety check
        return check_safety(exclude(row, outliers[0])) or check_safety(exclude(row, outliers[1]))
    else:
        return False


def main():
    with open('2_input.txt', 'r') as f:
        lines = list(map(lambda x: list(map(int, x.strip('\n').split(' '))), f.readlines()))
    print(sum(map(int, map(check_safety, lines))))
    print(sum(map(int, map(check_safety_dampener, lines))))


if __name__ == '__main__':
    main()
