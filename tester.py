
import os
from subprocess import Popen, PIPE, STDOUT
from colorama import Fore, Style
from random import randrange


# Whether or not the tests should run for a bonus submission
# (if false, inputs limited to 100 characters)
run_for_bonus = False


def run_calculator(in_str: str, expected: int):
    p = Popen(['./calc'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=(in_str + '\n').encode())[0]
    assert grep_stdout.decode() == f'Result is: {expected}\n', f'{in_str} = {expected}'


def test_basic():
    run_calculator('(1)', 1)
    run_calculator('(-1)', -1)
    run_calculator('(1--1)', 2)
    run_calculator('(1-(-1))', 2)
    run_calculator('((2+3)*2))', 10)
    run_calculator('((1*2)/(3-5))', -1)
    run_calculator('(1+(1+(1+(1+1))))', 5)
    run_calculator('(1+1)', 2)
    run_calculator('(1--1)', 2)
    run_calculator('((2/3)+5)', 5)
    run_calculator('(((-5/2)*-2)+(-4))', 0)
    run_calculator('', 0)


def test_add():
    run_calculator('(1+1)', 2)
    run_calculator('(-1+-2)', -3)
    run_calculator('(-1+2)', 1)
    run_calculator('(1+-2)', -1)
    run_calculator('(-1+-20)', -21)
    run_calculator('((-1+-2)+(-8+0))', -11)


def test_sub():
    run_calculator('(1-1)', 0)
    run_calculator('(-1--2)', 1)
    run_calculator('(-1-2)', -3)
    run_calculator('(1--2)', 3)
    run_calculator('(-1--20)', 19)


def test_mult():
    run_calculator('(1*1)', 1)
    run_calculator('(-1*-2)', 2)
    run_calculator('(-1*2)', -2)
    run_calculator('(1*-2)', -2)
    run_calculator('(-1*-20)', 20)


def test_div():
    run_calculator('(1/1)', 1)
    run_calculator('(-1/-2)', 0)
    run_calculator('(-2/-1)', 2)
    run_calculator('(-1/2)', 0)
    run_calculator('(-2/1)', -2)
    run_calculator('(1/-2)', 0)
    run_calculator('(2/-1)', -2)
    run_calculator('(-1/-20)', 0)
    run_calculator('(-20/-1)', 20)


def test_large():
    run_calculator('(9223372036854775807)', 9223372036854775807)
    run_calculator('(9223372036854775807+0)', 9223372036854775807)
    run_calculator('(9223372036854775807*1)', 9223372036854775807)
    run_calculator('(9223372036854775807/1)', 9223372036854775807)
    run_calculator('(9223372036854775807/(9223372036854775807/9223372036854775807))', 9223372036854775807)
    run_calculator('(9223372036854775807*(9223372036854775807/9223372036854775807))', 9223372036854775807)
    run_calculator('((9223372036854775807/9223372036854775807)*(9223372036854775807/9223372036854775807))', 1)
    run_calculator('((9223372036854775807/9223372036854775807)/(9223372036854775807/9223372036854775807))', 1)
    run_calculator('((9223372036854775806/9223372036854775807)*(9223372036854775807/9223372036854775807))', 0)
    run_calculator('((9223372036854775806/9223372036854775807)/(9223372036854775807/9223372036854775807))', 0)

    run_calculator('(-9223372036854775808)', -9223372036854775808)
    run_calculator('(-9223372036854775808+0)', -9223372036854775808)
    run_calculator('(-9223372036854775808*1)', -9223372036854775808)
    run_calculator('(-9223372036854775808/1)', -9223372036854775808)
    run_calculator('(-9223372036854775808/(-9223372036854775808/-9223372036854775808))', -9223372036854775808)
    run_calculator('(-9223372036854775808*(-9223372036854775808/-9223372036854775808))', -9223372036854775808)
    run_calculator('((-9223372036854775808/-9223372036854775808)*(-9223372036854775808/-9223372036854775808))', 1)
    run_calculator('((-9223372036854775808/-9223372036854775808)/(-9223372036854775808/-9223372036854775808))', 1)
    run_calculator('((-9223372036854775807/-9223372036854775808)*(-9223372036854775808/-9223372036854775808))', 0)
    run_calculator('((-9223372036854775807/-9223372036854775808)/(-9223372036854775808/-9223372036854775808))', 0)
    run_calculator('(9223372036854775807*0)', 0)
    run_calculator('(9223372036854775807*((9223372036854775807/9223372036854775807)-1))', 0)

    run_calculator('(9223372036854000000+775807)', 9223372036854775807)
    run_calculator('(-9223372036854000000+-775808)', -9223372036854775808)

    run_calculator('(2036854000000*775807)', 1580205591178000000)


def test_random():
    n = 100
    low = -10000
    high = 10000
    for i in range(n):
        a = randrange(low, high)
        b = randrange(low, high)
        c = randrange(low, high)
        d = randrange(low, high)
        e = randrange(low, high)
        if b == 0 or c == 0 or e == 0:
            continue
        run_calculator(f'((({a}*{b})/{c})+({d}/{e}))', int((a*b)/c) + int(d/e))
        run_calculator(f'((({a}/{b})*{c})*({d}*{e}))', (int(a / b) * c) * int(d * e))


def test_long():
    length = 240 if run_for_bonus else 24
    string = ""
    for i in range(length-1):
        string += '(6+'
    string += '6'
    for i in range(length-1):
        string += ')'
    run_calculator(string, 6*length)

    length = 240 if run_for_bonus else 24
    string = ""
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += '+6)'
    run_calculator(string, 6 * length)

    length = 100 if run_for_bonus else 10
    string = "("
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += '+6)'
    string += '+'
    for i in range(length-1):
        string += '(6+'
    string += '6'
    for i in range(length-1):
        string += ')'
    string += ')'
    run_calculator(string, 6 * length * 2)

    length = 100 if run_for_bonus else 10
    string = "("
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += '+6)'
    string += '-'
    for i in range(length-1):
        string += '(6+'
    string += '6'
    for i in range(length-1):
        string += ')'
    string += ')'
    run_calculator(string, 0)

    length = 100 if run_for_bonus else 10
    string = "("
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += '+6)'
    string += '*'
    for i in range(length - 1):
        string += '(6+'
    string += '6'
    for i in range(length - 1):
        string += ')'
    string += ')'
    run_calculator(string, (6 * length) ** 2)

    length = 100 if run_for_bonus else 10
    string = "("
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += '+6)'
    string += '/'
    for i in range(length - 1):
        string += '(6+'
    string += '6'
    for i in range(length - 1):
        string += ')'
    string += ')'
    run_calculator(string, 1)


def test_paren():
    length = 490 if run_for_bonus else 49
    string = ""
    for i in range(length - 1):
        string += '('
    string += '6'
    for i in range(length - 1):
        string += ')'
    run_calculator(string, 6)

    length = 450 if run_for_bonus else 45
    string = ""
    for i in range(length - 1):
        string += '('
    string += '(6+(1/1))'
    for i in range(length - 1):
        string += ')'
    run_calculator(string, 7)


tests = {'testBasic': test_basic,
         'testAddition': test_add,
         'testSubtraction': test_sub,
         'testMultiplication': test_mult,
         'testDivision': test_div,
         'testLarge': test_large,
         'testRandom': test_random,
         'testLong': test_long,
         'testParenthesis': test_paren}

if __name__ == '__main__':

    print(f"{Fore.YELLOW}Compiling.{Style.RESET_ALL}")
    print()
    os.system('make -s calc')

    numPassed = 0
    for (name, test) in tests.items():
        try:
            test()
            numPassed += 1
            print(f"{Fore.BLUE}Passed {name}.{Style.RESET_ALL}")
        except AssertionError as error:
            print(f"{Fore.RED}Failed {name} at assertion: {error.args[0]}{Style.RESET_ALL}")

    print()
    if numPassed == len(tests):
        print(f"{Fore.BLUE}Passed {numPassed} out of {len(tests)} tests.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Passed {numPassed} out of {len(tests)} tests.{Style.RESET_ALL}")
