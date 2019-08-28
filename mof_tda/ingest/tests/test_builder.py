# Copyright 2019 (c), Toyota Research Institute, All rights reserved
import unittest
import os
import shutil

# Set test environ
os.environ["MOF_TDA_DB_MODE"] = "test"

from mof_tda import MOF_TDA_TEST_FILE_PATH, MOF_TDA_PATH
from mof_tda.ingest.builder import MofDbStructureBuilder, PersistenceBuilder
from mof_tda.ingest.docdb import get_db
from monty.tempfile import ScratchDir
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

    def test_persistence_builder(self):
        # Set up structure collection

        structures = ["CICYIX_clean", "ZITWIK01_clean", "ZUTBAR03_clean"]
        with ScratchDir('.') as structure_dir:
            for name in structures:
                shutil.copy(os.path.join(
                    MOF_TDA_PATH, "all_MOFs", "{}.cif".format(name)), '.')
            structure_builder = MofDbStructureBuilder(
                structure_directory=structure_dir,
                structure_collection=self.test_db.structures)
            runner = Runner([structure_builder])
            runner.run()

            persistence_builder = PersistenceBuilder(
                structure_collection=self.test_db.structures,
                persistence_collection=self.test_db.persistence)
            items = persistence_builder.get_items()
            self.assertEqual(items.count(), 3)
            processed = []
            for item in items:
                processed.append(persistence_builder.process_item(item))
                import nose; nose.tools.set_trace()


if __name__ == '__main__':
    unittest.main()
