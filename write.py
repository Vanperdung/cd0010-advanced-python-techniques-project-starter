"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import cd_to_datetime, datetime_to_str

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    # TODO: Write the results to a CSV file, following the specification in the instructions.
    with open(filename, 'w') as cad_csv:
        writer = csv.DictWriter(cad_csv, fieldnames=fieldnames)
        writer.writeheader()
        
        for approach in results:
            row = {
                'datetime_utc': datetime_to_str(approach.time),
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name is not None else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter is not None else 'nan',
                'potentially_hazardous': 'True' if approach.neo.hazardous else 'False'
            }
            writer.writerow(row)
        
def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    cad_list = []

    for approach in results:
        approach_data = {
            'datetime_utc': datetime_to_str(approach.time),
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name is not None else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter is not None else float('nan'),
                'potentially_hazardous': bool(approach.neo.hazardous)
            }
        }
        cad_list.append(approach_data)

    with open(filename, 'w') as jsonfile:
        json.dump(cad_list, jsonfile, indent=4)
