import unittest
import os
from tempfile import NamedTemporaryFile
from csv import writer

from mergecsv import merge_csvs, check_headers


class TestCSVFunctions(unittest.TestCase):

    def setUp(self):
        # Create temporary CSV files for testing
        self.csv1 = NamedTemporaryFile(delete=False, mode='w', newline='')
        self.csv2 = NamedTemporaryFile(delete=False, mode='w', newline='')
        self.output_csv = NamedTemporaryFile(delete=False, mode='w', newline='')

        # Write headers to csv1 and csv2
        csv_writer = writer(self.csv1)
        csv_writer.writerow(['Name', 'Age', 'City'])
        self.csv1.flush()

        csv_writer = writer(self.csv2)
        csv_writer.writerow(['Name', 'Age', 'City'])
        self.csv2.flush()

    def tearDown(self):
        # Clean up the temporary files
        os.remove(self.csv1.name)
        os.remove(self.csv2.name)
        # Remove self.output_csv.name only if it exists
        if os.path.exists(self.output_csv.name):
            os.remove(self.output_csv.name)

    def test_check_headers_identical(self):
        # Test case where headers are identical
        result = check_headers(self.csv1.name, self.csv2.name)
        self.assertTrue(result)

    def test_check_headers_different(self):
        # Test case where headers are different
        self.csv2.truncate(0)  # Clear csv2
        csv_writer = writer(self.csv2)
        csv_writer.writerow(['Full Name', 'Age', 'City'])  # Different header
        self.csv2.flush()

        result = check_headers(self.csv1.name, self.csv2.name)
        self.assertFalse(result)

    def test_merge_csvs_identical_headers(self):
        # Test case where headers are identical and merge is successful
        merge_result, message = merge_csvs(self.csv1.name, self.csv2.name, self.output_csv.name)
        self.assertEqual(merge_result, 0)
        self.assertTrue(os.path.exists(self.output_csv.name))

    def test_merge_csvs_different_headers(self):
        # Test case where headers are different and merge fails
        self.csv2.truncate(0)  # Clear csv2
        csv_writer = writer(self.csv2)
        csv_writer.writerow(['Full Name', 'Age', 'City'])  # Different header
        self.csv2.flush()

        # Remove file self.output_csv.name if it exists
        if os.path.exists(self.output_csv.name):
            os.remove(self.output_csv.name)
        merge_result, message = merge_csvs(self.csv1.name, self.csv2.name, self.output_csv.name)
        self.assertEqual(merge_result, 1)


if __name__ == '__main__':
    unittest.main()

