import json
import sys

OUTPUT_DIR = '../outputs/'

neighbors_modified_file = OUTPUT_DIR+'neighbor-districts-modified.json'
json_file = open(neighbors_modified_file)
neighbors_modified_json = json.load(json_file)

set_tup = set()
for district, neighbors in neighbors_modified_json.items():
    for neighbor in neighbors:
        tup = [district, neighbor]
        tup.sort()
        set_tup.add(tuple(tup))

original_stdout = sys.stdout # Save a reference to the original standard output
with open(OUTPUT_DIR+'edge-graph.csv', 'w') as file:
    sys.stdout = file # Change standard_output to edge-graph.csv we created to print to the csv file instead of standard output
    for tup in set_tup:
        print(tup[0]+','+tup[1])
    sys.stdout = original_stdout # Reset the standard output to its original value