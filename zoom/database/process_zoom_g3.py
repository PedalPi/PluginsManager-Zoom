import json
import csv


plugins_categories = {}

with open('plugins_categories.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    header = True
    for row in csv_reader:
        if header:
            header = False
            continue

        plugins_categories[row[1]] = {
            'id': int(row[0]),
            'category': row[2],
        }

filename = 'From XML ZoomG3v2.json'

with open(filename) as data_file:
    data_list = json.load(data_file)

data = {
    107: {
        "name": "None",
        "category": "None",
        "parameters": [],
        "id": 107
    }
}

for element in data_list:
    index = plugins_categories[element['name']]['id']
    data[index] = element
    del element['offset']

    data[index]['id'] = index

    for parameter in element['parameters']:
        del parameter['offset']
        parameter['min'] = 0
        parameter['max'] = int(parameter['max'])
        parameter['default'] = int(parameter['default'])
        parameter['step'] = 1


print(json.dumps(data))
# python process_zoom_g3.py >> ZoomG3v2.json