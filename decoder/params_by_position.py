import json


def params_with_max_value_by_position(total_of_params=8):
    """
    To decode response message, is necessary discover the plugins with most param value per param position
    """
    effects = []
    with open('zoom/database/ZoomG3v2.json') as file:
        plugins = json.load(file)

    for i in range(total_of_params):
        effect = ''
        effect_id = -1
        max_value = 0

        for effect_name, effect_data in plugins.items():
            if len(effect_data['parameters']) <= i:
                continue

            if effect_data['parameters'][i]['max'] > max_value:
                effect = effect_name
                effect_id = effect_data['id']
                max_value = effect_data['parameters'][i]['max']

        effects.append((effect, effect_id, max_value))

    return effects
