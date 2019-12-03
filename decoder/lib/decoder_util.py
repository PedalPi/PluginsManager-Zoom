from itertools import count


def decode_message(data, bits_location):
    value = 0
    for position, mask, shift in bits_location:
        if shift == 'NZ':
            continue

        value |= shift_bits(data[position] & mask, shift)

    return value


def shift_bits(bits: int, total: int):
    if total > 0:
        return bits << total
    else:
        return bits >> abs(total)


def total_zero_bits_left(bits):
    i = 0
    for i in count():
        if bits != bits >> i << i:
            break
    return i - 1
