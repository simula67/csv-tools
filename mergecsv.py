import argparse
import csv


# Function to merge multiple CSV files without duplicating the headers
def merge_csvs(input_csvs, output_csv):

    # Check if all CSV files have the same headers
    if not check_headers(input_csvs):
        return 1, "Error: CSV files have different headers."

    with open(output_csv, 'w') as out:
        header_written = False
        for input_csv in input_csvs:
            with open(input_csv, 'r') as f:
                for line_number, line in enumerate(f):
                    if line_number == 0 and header_written:
                        continue
                    if line_number == 0:
                        header_written = True
                    out.write(line)
    return 0, "CSV files merged successfully."


# Check if all CSV files have the same headers
def check_headers(input_csvs):
    with open(input_csvs[0], 'r') as f:
        reader = csv.reader(f)
        reference_header = next(reader)

    for input_csv in input_csvs[1:]:
        with open(input_csv, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            if header != reference_header:
                return False
    return True


if __name__ == '__main__':
    # Accept command line arguments (using argparse) for multiple CSVs and merge them
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csvs', nargs='+', help='Input CSV files')
    parser.add_argument('output_csv', help='Output CSV file')
    args = parser.parse_args()
    merge_csvs(args.input_csvs, args.output_csv)
