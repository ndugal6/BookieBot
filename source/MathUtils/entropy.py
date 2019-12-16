import numpy as np
import math
import matplotlib.pyplot as plt

def entropy(count1, count2):
    """Return the entropy of binary system"""
    p1 = count1 / (count1 + count2)
    p2 = count2 / (count1 + count2)
    if 0 in [p1,p2]:
        return 0
    print(p1)
    ep1 = -1*p1 * math.log2(1)
    ep2 = -1*p2 * math.log2(1)
    return ep1 + ep2

def entropy_multi_variate(counts):
    """Return the entropies of multi variate systems, using static log base of 2"""
    proportions = []
    e = 0
    for count in counts:
        proportions.append(count / sum(counts))
    for proportion in proportions:
        e += 0 if proportion == 0 else ent(proportion)
    return e

def entropy_multi_variate2(counts):
    """Return the entropies of multi variate systems, using dynamic log base of # distinct elements in system"""
    proportions = []
    e = 0
    for count in counts:
        proportions.append(count / sum(counts))
    for proportion in proportions:
        e += 0 if proportion == 0 else ent(proportion, len(proportions))
    return e

def ent(value, base = 2):
    return -1 * value * math.log(value, base)

def get_array_of_counts(num):
    pass
    """dont remember where I was going with this function. leaving it here for now since it may come back to me"""


if __name__ == '__main__':
    es = list()
    for count1 in range(0,110,10):
        count2 = 100 - count1
        counts = [count1, count2/2, count2/2]
        es.append((count1, entropy_multi_variate(counts)))
    entropies_static_base = np.array(es)
    es = list()
    for count1 in range(0,110,10):
        count2 = 100 - count1
        counts = [count1, count2/2, count2/2]
        es.append((count1, entropy_multi_variate2(counts)))
    entropies_dynamic_base = np.array(es)
    plt.figure()
    plt.title('Entropy over Proportion Growth')
    # plt.xlim(-10,100)
    plt.xlabel('Percentage of solution')
    plt.ylabel('Entropy of System')
    # plt.ylim(-0.5, 1.5)
    plt.plot(entropies_static_base[:, 0], entropies_static_base[:, 1], 'k--', entropies_dynamic_base[:, 0], entropies_dynamic_base[:, 1], 'k')
    plt.legend(('Static base 2', 'Dynamic log base'), loc='upper center', shadow=True)
    plt.show()