# Simple program I wrote for a once-off thing where I needed to extract all keys from an object stored in a .json file.
# Project: https://github.com/mudkipscience/rail_roulette

import json


def read_keys():
    with open('datastore.json', 'r') as file:
        data = json.load(file)
        return list(data['unvisited'].keys())


def write_keys(keys):
    with open('keys.json', 'w') as file:
        json.dump(keys, file, indent=4, sort_keys=True)


def main():
    keys = read_keys()
    write_keys(keys)


main()
