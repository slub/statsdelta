#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import collections
import csv
import sys
import uuid

QUOTECHAR = '"'

CHANGED = 'changed'
NOT_CHANGED = 'not changed'
ADDED = 'added'
DELETED = 'deleted'

DIFF_HEADER = 'diff status'


def parse_csv(file_name, key_field, csv_dialect_name):
    csv_dict = {}
    header = []
    with open(file_name, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, dialect=csv_dialect_name)
        header_sampled = False
        for row in csvreader:
            csv_dict[row[key_field].strip()] = row
            if not header_sampled:
                header = row.keys()
                header_sampled = True

    return csv_dict, header


def header_in_output_fields(header, output_fields):
    for output_field in output_fields:
        if output_field not in header:
            return False

    return True


def run():
    parser = argparse.ArgumentParser(prog='statsdelta',
                                     description='Returns a delta statistic of two given statistics',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-from', type=str,
                                    help='The file to use as the left or from source for the delta calculation',
                                    dest='from_file', required=True)
    required_arguments.add_argument('-to', type=str,
                                    help='The file to use as the right or to source for the delta calculation',
                                    dest='to_file', required=True)
    required_arguments.add_argument('-key-field', type=str, help='The key field name (column name)', dest='key_field', required=True)

    optional_arguments.add_argument('-delimiter', type=str, default=',',
                                    help='The field delimiter used within the file; use TAB for tab-delimited')
    optional_arguments.add_argument('-output-fields', type=str,
                                    help='The names of the fields (column names) to include in the delta output (if this argument is not specified, then the header from the "from" CSV file is taken)', dest='output_fields')
    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()

    from_file = args.from_file
    to_file = args.to_file
    key_field = args.key_field
    delimiter = args.delimiter

    output_fields = []
    if args.output_fields is not None:
        output_fields = args.output_fields.split(',')

    csv_dialect_name = 'csv_dialect_' + str(uuid.uuid4())
    csv.register_dialect(csv_dialect_name, delimiter=delimiter, quotechar=QUOTECHAR)

    from_dict_and_header = parse_csv(from_file, key_field, csv_dialect_name)
    from_dict = from_dict_and_header[0]
    from_header = from_dict_and_header[1]

    to_dict_and_header = parse_csv(to_file, key_field, csv_dialect_name)
    to_dict = to_dict_and_header[0]
    to_header = to_dict_and_header[1]

    if len(output_fields) == 0:
        for header in from_header:
            if header is not key_field:
                output_fields.append(header)

    if not header_in_output_fields(from_header, output_fields) or not header_in_output_fields(to_header, output_fields):
        parser.error(
            'not all output fields are included in FROM or TO header, please make sure that at least the specified output fields are part of both CSV files')

    delta_dict = {}
    delta_header = [key_field, DIFF_HEADER]

    for output_field in output_fields:
        delta_header.append('from_' + output_field)
        delta_header.append('to_' + output_field)
        delta_header.append('delta_' + output_field)

    for from_key, from_values in from_dict.items():
        delta_row = {}
        diff_value = NOT_CHANGED

        delta_row[key_field] = from_key.strip()

        if from_key in to_dict:
            to_values = to_dict[from_key]
            for output_field in output_fields:
                from_value = from_values[output_field]
                to_value = to_values[output_field]
                delta_value = "{0:.2f}".format(float(from_value) - float(to_value))
                delta_row['from_' + output_field] = from_value
                delta_row['to_' + output_field] = to_value
                final_delta_value = delta_value
                if float(delta_value) > 0:
                    final_delta_value = '+' + str(delta_value)
                delta_row['delta_' + output_field] = final_delta_value
                if delta_value != '0.00':
                    diff_value = CHANGED
        else:
            diff_value = DELETED
            for output_field in output_fields:
                delta_row['from_' + output_field] = from_values[output_field]
                delta_row['to_' + output_field] = None
                delta_row['delta_' + output_field] = '-' + from_values[output_field]

        delta_row[DIFF_HEADER] = diff_value

        delta_dict[from_key] = delta_row

    delta_keys = delta_dict.keys()

    for to_key, to_values in to_dict.items():

        if to_key not in delta_keys:
            delta_row = {}
            diff_value = ADDED

            delta_row[key_field] = to_key.strip()

            for output_field in output_fields:
                delta_row['from_' + output_field] = None
                delta_row['to_' + output_field] = to_values[output_field]
                delta_row['delta_' + output_field] = '+' + to_values[output_field]

            delta_row[DIFF_HEADER] = diff_value

            delta_dict[to_key] = delta_row

    sorted_delta_dict = collections.OrderedDict(sorted(delta_dict.items()))

    with sys.stdout as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=delta_header, dialect='unix')

        writer.writeheader()
        for delta_value in sorted_delta_dict.values():
            writer.writerow(delta_value)


if __name__ == "__main__":
    run()
