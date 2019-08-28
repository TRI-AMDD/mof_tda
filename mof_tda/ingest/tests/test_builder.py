# Copyright 2019 (c), Toyota Research Institute, All rights reserved
import unittest
import os

# Set test environ
os.environ["MOF_TDA_DB_MODE"] = "test"

from mof_tda import MOF_TDA_PATH, MOF_TDA_TEST_FILE_PATH
from mof_tda.ingest.builder import MofDbStructureBuilder
from mof_tda.ingest.docdb import get_db

from maggma.runner import Runner


class BuilderTest(unittest.TestCase):
    def setUp(self):
        self.test_db = get_db()
        self.test_db.structures.drop()
        self.test_db.persistence.drop()
        self.test_db.wasserstein_distances.drop()

    def tearDown(self):
        self.test_db.structures.drop()
        self.test_db.persistence.drop()
        self.test_db.wasserstein_distances.drop()

    def test_structure_builder(self):
        builder = MofDbStructureBuilder(source=MOF_TDA_TEST_FILE_PATH,
                                        target=self.test_db.structures)
        runner = Runner([builder])
        runner.run()


if __name__ == '__main__':
    unittest.main()
