import csv
from collections import defaultdict

from decoder.decoder_util import total_zero_bits_left
from decoder.diff import param_bits

effects = defaultdict(lambda: defaultdict(list))


with open('decoder/data_params.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    current_effect = 0
    current_param = 0

    for row in csv_reader:
        if len(row) == 2:
            current_effect, current_param = int(row[0]), int(row[1])
            continue

        effects[current_effect][current_param].append([int(e) for e in row])


effect_params_bits = []

for i, effect in effects.items():
    params_bits = []
    for j, param_data in effect.items():
        # filter all responses with len(data) > 40
        data = [d for d in param_data if len(d) > 40]

        # Ignore first message (old effect)
        bits = param_bits([d[:113] for d in data][1:])
        params_bits.append(bits)

    effect_params_bits.append(params_bits)



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
