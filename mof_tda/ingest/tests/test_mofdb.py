# Copyright 2019 (c), Toyota Research Institute, All rights reserved
import unittest
from mof_tda.ingest.mofdb import fetch_mofdb_isotherm, fetch_many_docs


class MofDbIngestionTest(unittest.TestCase):
    def test_json_fetch(self):
        # Test fetching of legit data
        isotherm = fetch_mofdb_isotherm(iso_id=23076)
        self.assertEqual(isotherm['temperature'], 77)

        # Test fetching of bad data
        isotherm = fetch_mofdb_isotherm(iso_id=23077)
        self.assertEqual(isotherm['temperature'], None)

        # Test multifetching
        isotherms = fetch_many_docs(iso_ids=[23076, 23077])
        self.assertEqual(isotherms[0]['temperature'], 77)
        self.assertEqual(isotherms[1]['temperature'], None)


if __name__ == '__main__':
    unittest.main()