import itertools
import re


def main():
    with open('3_input.txt', 'r') as f:
        data = f.read()

    number = r'[0-9]{1,3}'
    mul_regex = re.compile(rf'mul\(({number},{number})\)')
    muls = mul_regex.findall(data)
    res = sum(itertools.starmap(lambda w, z: w * z, map(lambda x: map(lambda y: int(y), x.split(',')), muls)))
    print(res)


if __name__ == '__main__':
    main()
