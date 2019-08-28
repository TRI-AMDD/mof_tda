# Copyright 2019 (c), Toyota Research Institute, All rights reserved
import unittest
import os

# Set test environ
os.environ["MOF_TDA_DB_MODE"] = "test"

from mof_tda import MOF_TDA_PATH
from mof_tda.ingest.docdb import add_isotherms_to_database, get_db


class MofDbIngestionTest(unittest.TestCase):
    def setUp(self):
        self.test_db = get_db()
        self.test_db['isotherms'].drop()

    def tearDown(self):
        self.test_db['isotherms'].drop()

    def test_add_isotherms_to_db(self):
        add_isotherms_to_database(os.path.join(
            MOF_TDA_PATH, "ingest", "mofdb_isotherms", "example_mofdb.json"))
        doc = self.test_db.isotherms.find_one({"adsorbent.name": "FECWOB_clean"})
        self.assertIsNotNone(doc, "Cannot find inserted document")
        self.assertEqual(self.test_db.isotherms.find().count(), 2)
        self.assertEqual(doc["isotherm_data"][0]["pressure"], 10)


if __name__ == '__main__':
    unittest.main()
