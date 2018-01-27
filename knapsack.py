"""
This file includes various implementations of Knapsack.

# Usage example
# creating a random kp instance
kp_instance = random_kp_instance(5, 100, 10)
kp_print(*kp_instance)

# recursive_kp
print('\n*recursive_kp function*')
recursive_P = recursive_kp(*kp_instance)
print(recursive_P)
print()

# dynamic_kp
print('\n*dynamic_kp function*')
dynamic_P, dynamic_items = dynamic_kp(*kp_instance)
print(dynamic_P, dynamic_items)
print()

# back_track_kp
print('\n*back_track_kp function*')
back_track_P = 0
back_track_items = None
back_track_kp(*kp_instance)
print(back_track_P, back_track_items)
print()

# approx_kp
print('\n*approx_kp function*')
epsilon = .4
approx_P, approx_items = approx_kp(*kp_instance, epsilon)
print('epsilon: {}'.format(epsilon))
print(approx_P, approx_items)
print()
"""
__author__ = "Mohammad Sadegh Ghasemi"
__date__ = "2018-01-19"


def recursive_kp(Z, wt, p, n):
    """A naive recursive implementation of 0-1 Knapsack Problem.

    Time complexity:
        2^n (exponential)

    Args:
        Z (int, float): the capacity of the Knapsack
        wt (list): the items weight list
        p (list) : the items profit
        n (int): the number of items (it's equal to len(wt) = len(p))

    Returns:
        maximum_profits: the maximum profits that can be put in a knapsack
        of capacity Z
    """

    if n == 0 or Z == 0:
        return 0

    if (wt[n - 1] > Z):
        return recursive_kp(Z, wt, p, n - 1)

    return max(
        p[n - 1] + recursive_kp(Z - wt[n - 1], wt, p, n - 1),
        recursive_kp(Z, wt, p, n - 1)
    )


def dynamic_kp(Z, wt, p, n):
    """A dynamic implementation of 0-1 Knapsack Problem.

    Time Complexity:
        O(nZ) where n is the number of items and Z is the capacity of knapsack.

    Args:
        Z (int, float): the capacity of the Knapsack
        wt (list): the items weight list
        p (list) : the items profit
        n (int): the number of items (it's equal to len(wt) = len(p))

    Returns:
        (
            maximum_profits: the maximum profits that can be put in a
                knapsack of capacity Z,
            picked_items: a list of selected items
        )
    """
    import numpy as np
    # it's imported here because it used nowhere else.
    # it does not seem logical ;D

    K = np.zeros((n + 1, Z + 1))
    keep = np.zeros((n + 1, Z + 1))

    # Build table K[][] in bottom up manner
    for i in range(1, n + 1):
        for w in range(1, Z + 1):
            if (
                wt[i - 1] <= w and
                p[i - 1] + K[i - 1, w - wt[i - 1]] > K[i - 1, w]
            ):
                K[i, w] = p[i - 1] + K[i - 1, w - wt[i - 1]]
                keep[i, w] = 1
            else:
                K[i, w] = K[i - 1, w]

    j = Z
    picked_items = []
    for i in range(n, 0, -1):
        if keep[i, j] == 1:
            picked_items.append(i)
            j -= wt[i - 1]

    picked_items.reverse()

    return K[n, Z], picked_items


def approx_kp(Z, wt, p, n, epsilon=.4):
    """FPTAS (fully polynomial time approximation scheme) for 0-1 Knapsack
    Problem using dynamic programming.
    The solution of this algorithm falls within a (1 − epsilon) factor of OPT.
    P(S') ≥ (1 − epsilon) · OPT.

    Time Complexity:
        The running time of the algorithm is O(n^2 · floor(n/epsilon)),
        which is polynomial both n and 1/epsilon.

    Args:
        Z (int, float): the capacity of the Knapsack
        wt (list): the items weight list
        p (list) : the items profit
        n (int): the number of items (it's equal to len(wt) = len(p))
        epsilon (float): the error parameter in range (0, 1]
    Returns:
        (
            approx maximum_profits: the maximum profits that can be
                put in a knapsack of capacity Z,
            picked_items: a list of selected items
        )
    """

    theta = epsilon * max(p) / n
    v = [vi // theta for vi in p]
    _P, approx_items = dynamic_kp(Z, wt, v, n)
    approx_P = sum([p[i - 1] for i in approx_items])

    return approx_P, approx_items


def back_track_kp(Z, wt, p, n, x=None, level=0, cur_w=0):
    """
    Important:
        It is not a good way but this function works with two global
        variables "back_track_items", "back_track_P".
        so before calling this function please run the following lines:
        back_track_items = None
        back_track_P = 0

    Args:
        Z (int, float): the capacity of the Knapsack
        wt (list): the items weight list
        p (list) : the items profit
        n (int): the number of items (it's equal to len(wt) = len(p))

    Returns:
        This function saves the maximum_profits and picked_items in two global
        variables "back_track_items", "back_track_P". so before calling this
        function please run the following lines:
        back_track_items = None
        back_track_P = 0
        the back_track_items is a binary list that shows if an item is
        selected by algorithm or not.
    """
    if level == n:
        global back_track_items
        global back_track_P
        profit = sum([p[i] for i in range(n) if x[i]])
        if profit > back_track_P:
            back_track_items = x
            back_track_P = profit
    else:
        try:
            x_tmp = x[:]
        except TypeError:
            x_tmp = [0] * n
        x_tmp[level] = 0
        back_track_kp(Z, wt, p, n, x_tmp, level=level + 1, cur_w=cur_w)

        if wt[level] + cur_w <= Z:
            x_tmp[level] = 1
            back_track_kp(Z, wt, p, n, x_tmp, level=level + 1,
                          cur_w=wt[level] + cur_w)


def random_kp_instance(n=10, profit_range=100, weight_range=10, Z=None):
    """
    Args:
        n (int): the number of items (it's equal to len(wt) = len(p))
        profit_range : a two-elements list or tuple as range of the
            items profits. both "start" and the "end" are inclusive.
            if an integer passed it considered as the "end". the default
            "start" is 1.
        weight_range : a two-elements list or tuple as range of the
            items weights. both "start" and the "end" are inclusive.
            if an integer passed it considered as the "end". the default
            "start" is 1.
        Z (int, float): the capacity of the Knapsack. by default it is
            a randomly selected integer from (1, sum(wt)) in which wt is
            the list of items weights and also both start and the end are
            inclusive.

    Returns:
        kp_instance: [Z, wt, p, n]
            Z: the capacity of the knapsack
            wt: a list of items weights
            p: a list of items profits
            n: the number of items
    """

    import random
    # it's imported here because it used nowhere else.
    # it does not seem logical ;D

    try:
        p_start, p_end = profit_range
    except TypeError:
        p_start, p_end = 1, profit_range
    try:
        w_start, w_end = weight_range
    except TypeError:
        w_start, w_end = 1, weight_range

    p = [random.randint(p_start, p_end) for x in range(n)]
    wt = [random.randint(w_start, w_end) for x in range(n)]
    if Z is None:
        Z = random.randint(1, sum(wt))

    return [Z, wt, p, n]


def kp_print(Z, wt, p, n):
    try:
        print(
            'Z (Capacity): {}\n'
            'p (profits): {}\n'
            'wt (weights): {}\n'
            'n (number of items): {}\n'.format(Z, p, wt, n)
        )
    except Exception:
        print('Please check the parameters')
