import sys, threading
from tokenize import group


def tokens():
    while True:
        for token in input().split():
            yield token

it = tokens()

def nextInt():
    return int(next(it))

def nextToken():
    return next(it)

def nextFloat():
    return float(next(it))

def solve():
    n = nextInt()
    k = nextInt()
    a = [0]*n
    for i in range(n):
        a[i] = nextInt()

    el_2_cnt = {}
    for _ in range(n):
        el_2_cnt[a[_]] = el_2_cnt.get(a[_], 0) + 1


    # print(cnt)
    cnt_to_group_size = {}
    for key in el_2_cnt:
        cnt_to_group_size[el_2_cnt[key]] = cnt_to_group_size.get(el_2_cnt[key], 0) + 1

    # print(group)

    # Can we go as is?
    uniq_elements = len(el_2_cnt)
    ans = 0
    # howMuch = next(iter(sorted(cnt_to_group_size)))

    # print("first", ans)
    delta = 0
    for howMuch in sorted(cnt_to_group_size):
        if abs(n - k) % uniq_elements == 0 and n - (howMuch - delta) * uniq_elements < k:
            ans += 1
            # print(1)
        n -= (howMuch - delta) * uniq_elements
        uniq_elements -= cnt_to_group_size[howMuch]
        delta = howMuch
        # testing difference

        # n -= cnt_to_group_size[g] * uniq_elements
        # uniq_elements -= cnt_to_group_size[g]
        # if uniq_elements != 0 and abs(n - k) % uniq_elements == 0:
        #     ans += 1

    print(ans)


def main():
    t = nextInt()
    while t > 0:
        t -= 1
        solve()

INCREASED_RECURSION_LIMIT = False

if INCREASED_RECURSION_LIMIT:
    sys.setrecursionlimit(1 << 25)
    threading.stack_size(1 << 27)
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
else:
    main()