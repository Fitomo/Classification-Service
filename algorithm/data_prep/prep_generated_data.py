import sys
import json
import csv

# Encodes files in utf-8
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def json_to_csv(json_file, output_file):
    fieldnames=['date', 'steps', 'user_id', 'total_sleep', 'resting_hr']
    with open(output_file, 'wb+') as file:
        dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
        dict_writer.writerow(dict(zip(fieldnames, fieldnames)))
        dict_writer.writerows(json_file)

def prep_data():
    # When calling the function from terminal, call:
    # python prep_generated_data.py output_file (all input files)
    output_file = sys.argv[1]
    all_training_data_json = []

    def create_usable_json_format(file, output_list):
        with open(file, 'rb') as unparsed_json:
            content = unparsed_json.read()
            parsed_json_file1 = json.loads(content, object_hook=byteify)
            for user in parsed_json_file1:
                for activities in parsed_json_file1[user]['activitiesLog']:
                    # Parse out necessary information and put it into a standard format
                    temp = {}
                    temp['user_id'] = user
                    temp['date'] = activities['date']
                    temp['steps'] = float(activities['steps'])
                    temp['total_sleep'] = float(activities['totalSleep'])
                    temp['resting_hr'] = float(activities['restingHR'])
                    output_list.append(temp)

    for file in sys.argv[2:]:
        create_usable_json_format(file, all_training_data_json)

    json_to_csv(all_training_data_json, output_file)

prep_data()
