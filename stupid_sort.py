__author__ = "Mohammad Sadegh Ghasemi"
__date__ = "2018-01-19"

from math import ceil


def stupid_sort(A, start=0, end=None):
    """This is a stupid sort. It works on original list A, so if
    you want the original list to be unchanged, send a copy of
    it to this function.

    Args:
        A (list): a list of numbers
        start: this variable is used for recursive calls.
        end: this variable is used for recursive calls.

    Returns:
        ascending sorted A

    example:
        import random
        my_list = [random.randint(1, 20) for i in range(10)]
        my_sorted_list = stupid_sort(my_list[:])
        print(my_list)
        print(my_sorted_list)
    """
    if end is None:
        end = len(A) - 1

    n = end - start + 1

    if n == 2 and A[start] > A[end]:
        A[start], A[end] = A[end], A[start]
    elif n > 2:
        m = ceil(2 * n / 3)
        stupid_sort(A, start, start + m - 1)
        stupid_sort(A, start + n - m, start + n - 1)
        stupid_sort(A, start, start + m - 1)

    return A
