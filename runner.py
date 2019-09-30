import sys

inf = 2 * 10 ** 5
inf_bin = len(bin(inf)[2:])


# Lets find amount of such substring in the given string (01 characters) where bit representation is equals of length
def pre_calculate_amount_of_zero_left(s):
    prefix = [0] * len(s)
    cur_amount = 0
    for i in range(0, len(s)):
        if s[i] == '0':
            cur_amount += 1
        elif s[i] == '1':
            prefix[i] = cur_amount
            cur_amount = 0
    return prefix


def solve_for_bit_len(string, pref, bit_len):
    ans = 0
    for i in range(0, len(string) - bit_len + 1):
        if string[i] == '1':
            num = int(string[i:i + bit_len], 2)
            rem = num - bit_len
            if num <= inf and rem <= pref[i]:
                ans += 1
    return ans


for _ in range(int(input())):
    s = str(input())
    amount_of_zero_left = pre_calculate_amount_of_zero_left(s)
    ans = 0
    for bit_len in range(1, inf_bin + 1):
        ans += int(solve_for_bit_len(s, amount_of_zero_left, bit_len))
    print(ans)
