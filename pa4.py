from statsmodels.sandbox.stats.runs import runstest_1samp
from scipy.stats import chisquare, kstest, wilcoxon
import math

def prime(p):
    for i in range(2, int(1e9)):
        if i * i > p:
            break
        if p % i == 0:
            return False
    return True


def selectpq(l=800, r=2000):
    gcd, p = int(1e8), (-1, -1)
    for p1 in range(l, r + 1):
        if not prime(p1) or not prime(2 * p1 + 1):
            continue
        for p2 in range(p1 + 1, r + 1):
            if not prime(p2) or not prime(2 * p2 + 1) or (p1 * p2) % 4 != 3:
                continue
            if math.gcd((p1 - 3) // 2, (p2 - 3) // 2) < gcd:
                gcd = math.gcd((p1 - 3) // 2, (p2 - 3) // 2)
                p = (p1, p2)
    return p


def print_list(li):
    for i in li[:-1]:
        print(i, end=", ")
    print(li[-1])


def count_freq(li):
    f = {}
    for i in li:
        if i not in f:
            f[i] = 1
        else:
            f[i] += 1
    r = []
    for k, v in f.items():
        r.append(v)
    return r


# Blum Blum Shub implementation
def BlumBlumShub(num_generations, p, q, seed):
    ret = []
    ret.append(seed)
    M = p * q
    for i in range(num_generations - 1):
        ret.append((ret[-1] * ret[-1]) % M)
    return ret


# Lagged Fibonacci Generator implementation
def gen_LFG(i, j, n, lfg):
    lfg_li = []
    lfg_mod = 1145
    for i1 in range(n):
        lfg_li.append((lfg[i - 1] + lfg[j - 1]) % lfg_mod)
        lfg = lfg[1:]
        lfg.append(lfg_li[-1])
    return lfg_li


# Select p, q, seed and number of elements to generate
p, q = selectpq()
print(p, q)
seed = 18
n = 1000
# Calculate Blum Blum Shub and print the list as the answer
li_bl = BlumBlumShub(n, p, q, seed)
freq_bl = count_freq(li_bl)
print_list(li_bl)
print("Runs test - p value for Blum Blum Shub : ", runstest_1samp(li_bl)[1])
print("Chisquare test - p value for Blum Blum Shub : ", chisquare(freq_bl))
# Lagged Fibonacci Generator
# Calculate LFG list and print the list as the answer
i, j, lfg = 3, 7, [5, 63, 72, 31, 421, 141, 54, 323, 26, 412, 14, 241]
li_lfg = gen_LFG(i, j, n, lfg)
print_list(li_bl)
freq_lfg = count_freq(li_lfg)
print("Runs test; p value for LFG : ", runstest_1samp(li_lfg)[1])
print("Chisquare test; p value for LFG : ", chisquare(freq_lfg))
