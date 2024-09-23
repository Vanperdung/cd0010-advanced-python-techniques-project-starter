"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_list = []
    
    with open(neo_csv_path, 'r') as neo_csv:
        neo_data = csv.DictReader(neo_csv)
        for row in neo_data:
            neo_row = NearEarthObject(**row)
            neo_list.append(neo_row)

    return neo_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    cad_list = []
    with open(cad_json_path, 'r') as cad_json:
        cad_data = json.load(cad_json)
        fields = cad_data['fields']
        data = cad_data['data']
        for row in data:
            row_mapped = dict(zip(fields, row))
            cad_row = CloseApproach(**row_mapped)
            cad_list.append(cad_row)

    return cad_list