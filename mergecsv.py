import argparse


# Function to merge two CSV files without duplicating the headers
def merge_csvs(input_csv1, input_csv2, output_csv):

    # Check if two CSV files have the same headers
    if not check_headers(input_csv1, input_csv2):
        return 1, "Error: CSV files have different headers."

    with open(input_csv1, 'r') as f1, open(input_csv2, 'r') as f2, open(output_csv, 'w') as out:
        for line in f1:
            out.write(line)
        header = True
        for line in f2:
            if header:
                header = False
                continue
            out.write(line)
    return 0, "CSV files merged successfully."


# Check if two CSV files have the same headers
def check_headers(input_csv1, input_csv2):
    with open(input_csv1, 'r') as f1, open(input_csv2, 'r') as f2:
        header1 = f1.readline().strip()
        header2 = f2.readline().strip()
    return header1 == header2


if __name__ == '__main__':
    # Accept command line arguments (using argparse) for two csvs and merge them
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv1', help='Input CSV file 1')
    parser.add_argument('input_csv2', help='Input CSV file 2')
    parser.add_argument('output_csv', help='Output CSV file')
    args = parser.parse_args()
    merge_csvs(args.input_csv1, args.input_csv2, args.output_csv)
