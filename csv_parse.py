import csv
import json
import os.path
import sys
import pprint

'''Super hacky script to parse the CSV files that the government generates...

Ugly but it works. '''

filename = ''
if len(sys.argv) < 1:
    print('You need to specify an input file to process.')
    exit()
else:
    filename = sys.argv[1]

def jsonify_csv(filename):
    with open(filename, 'r') as in_file:
        reader = csv.reader(in_file)
        rows = [row for row in reader if row[0]]
        rows = rows[1:]

        output = {}
        visited_nodes = []

        for row in rows:
            if 'Total' in row[0] and not output:
                output['name'] = row[0]
                output['children'] = []
                output['children'].append({'name': row[1], 'children': []})

            elif 'Total' in row[0]:
                if row[2]:
                    output['children'].append({'name': row[1], 'size': row[2]})
                else:
                    output['children'].append({'name': row[1], 'children': []})

            elif row[2]:
                for child in output['children']: #Check first layer for insert
                    if child['name'] == row[0]:
                        child['children'].append({'name': row[1], 'size': row[2]})
                    else:
                        if 'children' in child:
                            for sub_child in child['children']:
                                if sub_child['name'] == row[0]:
                                    sub_child['children'].append({'name': row[1], 'size': row[2]})


            else:
                for child in output['children']:
                    if child['name'] == row[0]:
                        child['children'].append({'name': row[1], 'children':[]})


    return output




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to specify an output directory and at least one input file')
        exit()

    output_dir = sys.argv[1]
    input_files = sys.argv[2:]

    for filename in input_files:
        root, ext = os.path.splitext(filename)
        final_output = jsonify_csv(filename)
        with open(os.path.join(output_dir, root + '.json'), 'w') as outfile:
            json.dump(final_output, outfile, indent=4)
