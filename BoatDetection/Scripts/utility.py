def sum(list):
    """
    list[any] -> float/int
    Returns the sum of every elements in a list.
    """

    total = 0

    for i in range(len(list)):
        total = total + list[i]

    return total