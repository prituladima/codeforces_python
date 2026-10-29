MOD = 10**9 + 7
def prepareCnk(n):
    f =[1]*(n + 1)
    iF = [1]*(n + 1)
    for i in range(2, n + 1, 1):
        f[i] = f[i - 1] * i % MOD
    iF[n] = pow(f[n], MOD - 2, MOD)
    for i in range(n - 1, 1, -1):
        iF[i] = iF[i + 1] * (i + 1) % MOD

    return f, iF

def preparePow2 (n):
    pow2 = [1]*(n + 1)
    for _ in range(1, n + 1, 1) :
        pow2[_] *= pow2[_ - 1] * 2 % MOD
    return pow2

# pow2 = preparePow2(200000 + 10)

def C(f, inv_f, n, k):
    return (f[n] * inv_f[n - k]) % MOD * inv_f[k] % MOD