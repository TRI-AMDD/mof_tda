# Copyright 2019 (c), Toyota Research Institute, All rights reserved
import unittest
import os

# Set test environ
os.environ["MOF_TDA_DB_MODE"] = "test"

from mof_tda import MOF_TDA_TEST_FILE_PATH
from mof_tda.ingest.builder import MofDbStructureBuilder, PersistenceBuilder
from mof_tda.ingest.docdb import get_db
from pymatgen import Structure
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
        builder = MofDbStructureBuilder(structure_directory=MOF_TDA_TEST_FILE_PATH,
                                        structure_collection=self.test_db.structures)
        self.assertEqual(len(builder.get_items()), 4)
        runner = Runner([builder])
        runner.run()
        coll = self.test_db.structures
        doc = coll.find_one({"name": "00958972.2016.1250260_1436516_clean"})
        self.assertIsNotNone(doc)
        structure = Structure.from_dict(doc['structure'])
        self.assertEqual(structure.lattice.a, 5.8405)
        self.assertEqual(coll.find().count(), 4)
        self.assertEqual(len(builder.get_items()), 0)
        runner.run()

    @unittest.skip
    def test_persistence_builder(self):
        # Set up structure collection
        structure_builder = MofDbStructureBuilder(
            structure_directory=MOF_TDA_TEST_FILE_PATH,
            structure_collection=self.test_db.structures)
        persistence_builder = PersistenceBuilder(
            structure_collection=self.test_db.structures,
            persistence_collection=self.test_db.structures)
        runner = Runner([structure_builder, persistence_builder])
        runner.run()


if __name__ == '__main__':
    unittest.main()
