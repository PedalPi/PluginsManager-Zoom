from itertools import count
from typing import List, Tuple


class Diff:

    def __init__(self, position, mask):
        self.position = position
        self.mask = mask

    def same_position(self, other: 'Diff'):
        return self.position == other.position

    def is_next(self, other: 'Diff'):
        """ :return: other is the next significant bit? """
        return other.mask == self.mask << 1

    def __or__(self, other: 'Diff'):
        if not self.same_position(other):
            raise Exception('Different position')

        return Diff(self.position, self.mask | other.mask)

    def __repr__(self):
        return f'({self.position}, {bin(self.mask)})'


def compare(base, other):
    """
    :return List[Diff]: All diff between base and other
    """
    return [Diff(i, j ^ k) for i, j, k in zip(count(), base, other) if j ^ k != 0]


def param_bits(data: List[Tuple[int]]):
    base = data[0]

    diffs: List[List[Diff]] = [compare(base, other) for other in data]

    # Make masks joining messages
    new_data = {}
    current_range = range(0)
    current_diff = diffs[1][0]

    for index, diffs_a, diffs_b in zip(count(), diffs[1:], diffs[2:]):
        if len(diffs_a) == 0:
            print(f'{index} - No diff detected!!!')
            continue

        if len(diffs_a) > 1 or len(diffs_b) > 1:
            print('Something wrong. More than one bit changed:')
            print(f'{diffs_a}\n{diffs_b}')

        diff_a = diffs_a[0]
        diff_b = diffs_b[0]

        if diff_a.same_position(diff_b) \
        and diff_a.is_next(diff_b):
            current_diff = current_diff | diff_b
            current_range = range(current_range.start, current_range.stop+1)
        else:
            new_data[current_range] = current_diff
            current_range = range(current_range.stop+1, index+1)
            current_diff = diff_b

    new_data[current_range] = current_diff

    return new_data
