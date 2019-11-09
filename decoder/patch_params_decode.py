import csv
from collections import defaultdict

from decoder.lib.decoder_util import total_zero_bits_left
from decoder.lib.diff import param_bits

effects = defaultdict(lambda: defaultdict(list))


def read_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        current_effect = 0
        current_param = 0

        # Read line
        for row in csv_reader:
            if len(row) == 2:
                current_effect, current_param = int(row[0]), int(row[1])
                continue

            message = [int(e) for e in row]
            effects[current_effect][current_param].append(message)

    return effects


def extract_diffs(effects):
    effect_params_bits  = []
    for i, effect in effects.items():
        params_bits = []
        for j, param_data in effect.items():
            # filter all responses with len(data) > 40
            filtered_data = [d for d in param_data if len(d) > 40]

            # Ignore final data
            filtered_data = [d[:113] for d in filtered_data]
            bits = param_bits(filtered_data)
            params_bits.append(bits)

        effect_params_bits.append(params_bits)
    return effect_params_bits

effects = read_file('data_params.csv')
effect_params_bits = extract_diffs(effects)
effects_data = []
for effect in effect_params_bits:
    params_data = []

    for param in effect:
        param_data = []
        current_position = 0

        for rng, diff in param.items():
            shift = current_position - total_zero_bits_left(diff.mask)
            total = (rng.stop + 1) - rng.start
            param_data.append((diff.position, diff.mask, shift))

            current_position += total

        params_data.append(param_data)
    effects_data.append(params_data)


print(effects_data)
