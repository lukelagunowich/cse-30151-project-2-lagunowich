from code_traceTM_lagunowich import *

# Check valid input

r = [
    'a plus',
    'aaa',
    10,
    4,
    1.43,
    True,
    True,
    [[['', 'q1', 'aaa']],
    [['a', 'q1', 'aa'], ['a', 'q2', 'aa']],
    [['aa', 'q1', 'a'], ['aa', 'q2', 'a'], ['aa', 'qrej', 'a']],
    [['aaa', 'q1', '_'], ['aaa', 'q2', '_'], ['aaa', 'qrej', '_']],
    [['aaa_', 'qrej', '_'], ['aa', 'qacc', 'a']]]
]

o = traceTM(infile='data_a_plus_lagunowich.csv', input='aaa')

for i in range(len(r)):
    assert r[i] == o[i]

# Check invalid input (not in language)

r = [
    'a plus',
    'aab',
    6,
    3,
    1.2,
    False,
    True,
    [[['', 'q1', 'aab']],
    [['a', 'q1', 'ab'], ['a', 'q2', 'ab']],
    [['aa', 'q1', 'b'], ['aa', 'q2', 'b'], ['aa', 'qrej', 'b']],
    [['aab', 'qrej', '_']]]
]

o = traceTM(infile='data_a_plus_lagunowich.csv', input='aab')

for i in range(len(r)):
    assert r[i] == o[i]


# Check invalid input (too long)

r = [
    'a plus',
    'aaaaaaaaaaaaaaaaaaaaaa',
    44,
    15,
    1.42,
    False,
    False
]

o = traceTM(infile='data_a_plus_lagunowich.csv', input='aaaaaaaaaaaaaaaaaaaaaa')

for i in range(len(r)):
    assert r[i] == o[i]
