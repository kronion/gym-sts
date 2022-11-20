import numpy as np

def to_binary_array(n: int, digits: int) -> np.ndarray:
    array = [0] * digits

    idx = 0
    n_copy = n
    while n_copy > 0:
        if idx >= digits:
            raise ValueError(
                f"{n} is too large to represent with {digits} binary digits"
            )

        n_copy, r = divmod(n_copy, 2)
        if r > 0:
            array[idx] = 1
        idx += 1

    return np.array(array, dtype=np.uint8)


def from_binary_array(array: list[int]) -> int:
    total = 0
    place_value = 1

    for digit in array:
        if digit == 1:
            total += place_value

        place_value *= 2

    return total
