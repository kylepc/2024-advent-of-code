from typing import Iterator, List, Callable, Tuple


def parse(sep: str, lines: List) -> Iterator:
    return map(lambda x: list(map(int, x.split(sep))), filter(lambda x: sep in x, lines))


def rules_predicate(rules: List[Tuple[int, int]]) -> Callable[[List[int]], bool]:
    def fn(x: List[int]) -> bool:
        def match_rule(rule: Tuple[int, int]) -> bool:
            first, second = rule
            nums = list(filter(lambda y: y in rule, x))
            fails = len(nums) > 1 and nums[0] != first
            return not fails
        return all(map(match_rule, rules))
    return fn


def part_one(rules, updates) -> int:
    meet_rules = filter(rules_predicate(list(rules)), updates)
    mid_points = map(lambda x: x[int(len(x) / 2)], meet_rules)
    return sum(mid_points)


def main():
    with open('5_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    rules = parse('|', lines)
    updates = parse(',', lines)
    print(part_one(rules, updates))


if __name__ == '__main__':
    main()
