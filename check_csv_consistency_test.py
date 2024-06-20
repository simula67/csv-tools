import unittest
import os
import csv
from tempfile import NamedTemporaryFile
from io import StringIO
from unittest.mock import patch
import logging

from check_csv_consistency import check_csv_consistency


class TestCheckCSVConsistency(unittest.TestCase):

    def setUp(self):
        # Create temporary CSV files for testing
        self.csv_valid = NamedTemporaryFile(delete=False, mode='w', newline='')
        self.csv_inconsistent_columns = NamedTemporaryFile(delete=False, mode='w', newline='')
        self.csv_exception = NamedTemporaryFile(delete=False, mode='w', newline='')

        # Write data to CSV files
        self.write_valid_csv()
        self.write_inconsistent_columns_csv()
        self.write_exception_csv()

    def tearDown(self):
        # Clean up the temporary files
        os.remove(self.csv_valid.name)
        os.remove(self.csv_inconsistent_columns.name)
        os.remove(self.csv_exception.name)

    def write_valid_csv(self):
        # Write valid CSV content
        csv_content = [
            ['Name', 'Age', 'City'],
            ['John Doe', '30', 'New York'],
            ['Jane Smith', '25', 'San Francisco']
        ]
        self.write_to_csv(self.csv_valid, csv_content)

    def write_inconsistent_columns_csv(self):
        # Write CSV with inconsistent columns
        csv_content = [
            ['Name', 'Age'],
            ['John Doe', '30', 'New York'],
            ['Jane Smith', '25', 'San Francisco']
        ]
        self.write_to_csv(self.csv_inconsistent_columns, csv_content)

    def write_exception_csv(self):
        # Write CSV that causes an exception during processing
        self.csv_exception.write("Invalid, CSV\n")  # Invalid format to cause exception
        self.csv_exception.flush()

    def write_to_csv(self, file, rows):
        csv_writer = csv.writer(file)
        for row in rows:
            csv_writer.writerow(row)
        file.flush()

    def test_check_csv_consistency_valid(self):
        # Test valid CSV file
        result = check_csv_consistency(self.csv_valid.name)
        self.assertTrue(result)

    def test_check_csv_consistency_inconsistent_columns(self):
        # Test CSV file with inconsistent columns
        result = check_csv_consistency(self.csv_inconsistent_columns.name)
        self.assertFalse(result)

    @patch('builtins.open', side_effect=Exception("Mocked exception"))
    def test_check_csv_consistency_exception(self, mock_open):
        # Test CSV file that causes an exception during processing
        result = check_csv_consistency(self.csv_exception.name)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

