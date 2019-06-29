import unittest


class MofDbIngestionTest(unittest.TestCase):
    def test_json_fetch(self):
        # Test fetching of legit data
        isotherm = fetch_mofdb_isotherm_data(id=23076)
        self.assertEqual(isotherm['temperature'], 77)

        # Test fetching of bad data
        isotherm = fetch_mofdb_isotherm_data(id=23077)
        self.assertEqual(isotherm['temperature'], None)


if __name__ == '__main__':
    unittest.main()
