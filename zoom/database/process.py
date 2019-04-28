import json


filename = 'From XML ZoomG3v2.json'

with open(filename) as data_file:
    data_list = json.load(data_file)

data = {}

for element in data_list:
    data[element['name']] = element
    del element['offset']

    for parameter in element['parameters']:
        del parameter['offset']
        parameter['min'] = 0
        parameter['max'] = int(parameter['max'])
        parameter['default'] = int(parameter['max'])
        parameter['step'] = 1

print(json.dumps(data))
# python process.py >> ZoomG3v2.json