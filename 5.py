from typing import List, Callable, Tuple


def parse(sep: str, lines: List) -> List[List[int]]:
    return list(map(lambda x: list(map(int, x.split(sep))), filter(lambda x: sep in x, lines)))


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


def fix(rules: List[Tuple[int, int]]) -> Callable[[List[int]], List[int]]:
    def fn(x: List[int]) -> List[int]:
        count = 0
        while not rules_predicate(rules)(x) and count < 20:
            for rule in rules:
                index_match = list(filter(lambda y: y[1] in rule, enumerate(x)))
                first, second = rule
                if len(index_match) > 1 and index_match[0][1] != first:
                    x[index_match[0][0]] = first
                    x[index_match[1][0]] = second
            count += 1
        return x
    return fn


def part_two(rules, updates) -> int:
    rules = list(rules)
    not_meet_rules = list(filter(lambda x: not rules_predicate(list(rules))(x), updates))
    meet_rules = list(map(fix(list(rules)), not_meet_rules))
    assert all(map(rules_predicate(list(rules)), meet_rules))
    mid_points = list(map(lambda x: x[int(len(x) / 2)], meet_rules))
    return sum(mid_points)


def main():
    with open('5_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    rules = parse('|', lines)
    updates = parse(',', lines)
    print(part_one(rules, updates))
    print(part_two(rules, updates))


if __name__ == '__main__':
    main()
