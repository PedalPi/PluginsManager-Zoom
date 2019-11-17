import csv
from collections import defaultdict

from decoder.lib.decoder_util import total_zero_bits_left
from decoder.lib.diff import param_bits

effects = defaultdict(list)


def read_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        current_effect = 0

        for row in csv_reader:
            if len(row) == 1:
                current_effect = int(row[0])
                continue

            effects[current_effect].append([int(e) for e in row])
    return effects


def extract_diffs(effects):
    effect_params_bits = []

    for i, effect in effects.items():
        # filter all responses with len(data) > 40
        filtered_data = [d for d in effect if len(d) > 40]

        # Ignore final data
        filtered_data = [d[:113] for d in filtered_data]
        # Ignore first message
        #filtered_data = filtered_data[1:]
        bits = param_bits(filtered_data)
        effect_params_bits.append(bits)
    return effect_params_bits


effects = read_file('data_effects.csv')
effect_params_bits = extract_diffs(effects)


# Join diffs
effects_data = []
for effect in effect_params_bits:
    param_data = []
    current_position = 0

    for rng, diff in effect.items():
        shift = current_position - total_zero_bits_left(diff.mask)
        total = (rng.stop + 1) - rng.start
        param_data.append((diff.position, diff.mask, shift))

        current_position += total

    effects_data.append(param_data)

print(effects_data)
