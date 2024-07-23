import unittest
import os
from tempfile import NamedTemporaryFile
from csv import writer

from mergecsv import merge_csvs, check_headers


class TestCSVFunctions(unittest.TestCase):
    def setUp(self):
        # Create temporary CSV files for testing
        self.csv_files = []
        for i in range(3):
            temp_csv = NamedTemporaryFile(delete=False, mode='w', newline='')
            self.csv_files.append(temp_csv)

        # Write headers to all CSV files
        for csv_file in self.csv_files:
            csv_writer = writer(csv_file)
            csv_writer.writerow(['Name', 'Age', 'City'])
            csv_file.flush()
            csv_file.close()  # Close after writing

        self.output_csv = NamedTemporaryFile(delete=False, mode='w', newline='')

    def tearDown(self):
        # Clean up the temporary files
        for csv_file in self.csv_files:
            if os.path.exists(csv_file.name):
                os.remove(csv_file.name)
        try:
            if os.path.exists(self.output_csv.name):
                os.remove(self.output_csv.name)
        except PermissionError as e:
            print(f'Preventing test failure due to permission error: {e}')

    def test_check_headers_identical(self):
        # Test case where headers are identical
        result = check_headers([csv_file.name for csv_file in self.csv_files])
        self.assertTrue(result)

    def test_check_headers_different(self):
        # Test case where headers are different
        with open(self.csv_files[1].name, 'w', newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['Full Name', 'Age', 'City'])  # Different header

        result = check_headers([csv_file.name for csv_file in self.csv_files])
        self.assertFalse(result)

    def test_merge_csvs_identical_headers(self):
        # Test case where headers are identical and merge is successful
        for csv_file in self.csv_files:
            with open(csv_file.name, 'a', newline='') as f:
                csv_writer = writer(f)
                csv_writer.writerow(['Alice', 30, 'New York'])
                csv_writer.writerow(['Bob', 25, 'Los Angeles'])

        merge_result, message = merge_csvs([csv_file.name for csv_file in self.csv_files], self.output_csv.name)
        self.assertEqual(merge_result, 0)
        self.assertTrue(os.path.exists(self.output_csv.name))

        # Verify the merged content
        with open(self.output_csv.name, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 7)  # 1 header + 2*3 data rows

    def test_merge_csvs_different_headers(self):
        # Test case where headers are different and merge fails
        with open(self.csv_files[1].name, 'w', newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['Full Name', 'Age', 'City'])  # Different header

        if os.path.exists(self.output_csv.name):
            try:
                os.remove(self.output_csv.name)
            except PermissionError as e:
                print(f'Preventing test failure due to permission error: {e}')
        merge_result, message = merge_csvs([csv_file.name for csv_file in self.csv_files], self.output_csv.name)
        self.assertEqual(merge_result, 1)
        self.assertEqual(message, "Error: CSV files have different headers.")


if __name__ == '__main__':
    unittest.main()
