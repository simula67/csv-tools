import csv
import argparse
import logging
import os


def setup_logging():
    """
    Setup logging configuration.
    """
    log_level = os.getenv('LOGLEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(level=numeric_level, format='[%(levelname)s] %(message)s')


def check_csv_consistency(csv_file):
    """
    Check if all records in a CSV file have the same number of columns.

    Args:
    - csv_file (str): Path to the CSV file to be checked.

    Returns:
    - bool: True if all records have consistent columns, False otherwise.
    """
    try:
        num_columns = None
        row_count = 0

        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)

            for row in reader:
                row_count += 1

                # Check number of columns consistency
                if num_columns is None:
                    num_columns = len(row)
                elif len(row) != num_columns:
                    error_msg = f"Inconsistent number of columns at row {row_count}. Expected {num_columns}, got {len(row)}"
                    logging.error(error_msg)
                    return False

        logging.info(f"All records in {csv_file} have consistent number of columns.")
        return True

    except Exception as e:
        logging.error(f"Exception occurred while processing {csv_file}: {str(e)}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check consistency of columns in a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file to be checked')

    args = parser.parse_args()

    setup_logging()
    success = check_csv_consistency(args.csv_file)

    if success:
        exit_code = 0
    else:
        exit_code = 1

    exit(exit_code)
