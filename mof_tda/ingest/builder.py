"""
This module provides a build procedure for the structures,
persistence diagrams, and wasserstein distances associated
with the MOFDB

"""
import argparse
import os
from glob import glob

from monty.json import jsanitize
from monty.tempfile import ScratchDir
from pymatgen import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from mof_tda import MOF_TDA_PATH
from mof_tda.ingest.docdb import get_db
from mof_tda.main import lattice_param, copies_to_fill_cell, \
    get_delaunay_simplices, take_square_root, get_persistence
import ase.io
from maggma.builder import Builder
from maggma.runner import Runner


class MofDbStructureBuilder(Builder):
    """
    Builder for MOF DB structures
    """
    def __init__(self, structure_directory, structure_collection,
                 incremental=True, **kwargs):
        self.structure_directory = structure_directory
        self.output_collection = structure_collection
        self.incremental = incremental
        # Lazy init
        super().__init__(sources=[],
                         targets=[],
                         **kwargs)

    def get_items(self):
        pattern = os.path.join(self.structure_directory, "*.cif")
        all_filenames = glob(pattern)
        # TODO: implement md5 incremental determination?
        if self.incremental:
            all_names = [self.get_name_from_path(path)
                         for path in all_filenames]
            old_names = set(self.output_collection.distinct("name"))
            new_pairs = [(filename, name)
                         for filename, name in zip(all_filenames, all_names)
                         if name not in old_names]
            if new_pairs:
                return list(zip(*new_pairs))[0]
            else:
                return []
        else:
            return all_filenames

    def process_item(self, item):
        structure = Structure.from_file(item)
        name = self.get_name_from_path(item)
        doc = {"name": name,
               "structure": structure}
        return doc

    def update_targets(self, items):
        sanitized = jsanitize(items, strict=True)
        self.output_collection.insert_many(sanitized)

    @staticmethod
    def get_name_from_path(path):
        name = os.path.split(path)[-1]
        name = os.path.splitext(name)[0]
        return name


class PersistenceBuilder(Builder):
    """
    Builder for MOF DB persistence diagrams
    """
    def __init__(self, structure_collection, persistence_collection,
                 incremental=True, **kwargs):
        self.structure_collection = structure_collection
        self.persistence_collection = persistence_collection
        self.incremental = incremental
        # Lazy init
        super().__init__(sources=[],
                         targets=[],
                         **kwargs)

    def get_items(self):
        if self.incremental:
            new_names = set(self.structure_collection.distinct("name")) - \
                set(self.persistence_collection.distinct("name"))
            import nose; nose.tools.set_trace()
            return self.structure_collection.find(
                {"name": {"$in": list(new_names)}})
        else:
            return self.structure_collection.find()

    def process_item(self, item):
        structure = Structure.from_dict(item['structure'])
        persistence = self.get_persistence_from_structure(structure)
        return {"name": item['name'],
                "persistence": persistence
                }

    def update_targets(self, items):
        sanitized = jsanitize(items, strict=True)
        self.persistence_collection.insert_many(sanitized)

    @staticmethod
    def get_persistence_from_structure(structure):
        # TODO: we should really have a method which converts
        #       a native python object to persistence, rather than
        #       using files as an intermediate.  The consequence here
        #       is that we're stressing the filesystem unnecessarily
        #       and the logic isn't modular at all
        with ScratchDir('.'):
            import nose; nose.tools.set_trace()
            atoms = AseAtomsAdaptor.get_atoms(structure)
            ase.io.write("temp_structure.xyz", atoms)
            cubic_cell_dimension = 20
            xyz_file = "temp_structure.xyz"
            lattice_csts = lattice_param(xyz_file)
            new_cell = copies_to_fill_cell(cubic_cell_dimension, xyz_file, lattice_csts)
            simplices = get_delaunay_simplices(new_cell)
            simplices = take_square_root(simplices)
            persistence = get_persistence(simplices)

        return persistence


class WassersteinDistanceBuilder(Builder):
    """
    Builder for MOF DB structures
    """
    def __init__(self, source, target, incremental=True):
        self.source = source
        self.target = target
        self.incremental = incremental
        raise NotImplementedError(
            "Wasserstein Distance builder has not yet been implemented")

    def get_items(self):
        pass

    def process_item(self, item):
        pass

    def update_targets(self):
        pass


DEFAULT_STRUCTURE_DIR = os.path.join(MOF_TDA_PATH, "all_MOFs")


def get_runner(structure_directory=DEFAULT_STRUCTURE_DIR,
               persistence=True, wasserstein=False,
               incremental=True, database=None, **kwargs):
    """
    Function to get a runner that runs all of the builders
    in sequence

    Args:
        structure_directory (str): directory corresponding to structure
            files associated with the builder
        persistence (bool): whether to have a persistence builder
            in the runner sequence
        wasserstein (bool): whether to have a wasserstein builder
            in the runner sequence
        incremental (bool): whether the runners are incremental
            or total rebuilds
        database (Database): pymongo database object for the build
        **kwargs: kwargs for the Runner class

    Returns:
        (Runner) runner object for the database build

    """
    database = database or get_db()
    builders = []
    if structure_directory:
        builder = MofDbStructureBuilder(
            source=structure_directory,
            target=database.structures,
            incremental=incremental
        )
        builders.append(builder)

    if persistence:
        builder = PersistenceBuilder(
            source=database.structures,
            target=database.persistence,
            incremental=incremental
        )
        builders.append(builder)

    if wasserstein:
        builder = WassersteinDistanceBuilder(
            source=database.structures,
            target=database.persistence,
            incremental=incremental
        )
        builders.append(builder)

    return Runner(builders, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--structure", action="store_true",
                        help="Build structure database")
    parser.add_argument("-p", "--persistence", action="store_true",
                        help="Build persistence database")
    parser.add_argument("-w", "--wasserstein", action="store_true",
                        help="Build Wasserstein distance database")
    parser.add_argument("-i", "--incremental", action="store_true",
                        help="Whether builder(s) are incremental")
    args = parser.parse_args()
    runner = get_runner(args.structure,
                        args.persistence,
                        args.wasserstein,
                        args.incremental)
    runner.run()
