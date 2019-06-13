import numpy as np
import hashlib #debugging
from typing import (Any, Set, List, Tuple, Dict, Optional, TextIO)
import dionysus as d
import diode
from create_cubic_cells import copies_to_fill_cell, lattice_param

MOF_FILES = 'subset_mof_list.txt'
filepaths = []
with open(MOF_FILES,'r') as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4] #strip .cif off
        filepaths.append(stripped_line + ".xyz")

def get_delaunay_simplices(points : List[List]) -> List[List]:
    """
    Convert coordinates to simplicial complex using alpha shapes
    Args:
        points: list of coordinates
    Return:
        simplices: list of simplicial complexes
    """
    simplices = diode.fill_alpha_shapes(points)
    return simplices

def get_filtration( simplices : List[List]) -> Any:
    """
    Calculate filtration from simplicial complexes
    Args:
        simplices: list of simplicial complexes
    Return:
        Filtration output
    """
    f = d.Filtration()
    for vertices, time in simplices:
        f.append(d.Simplex(vertices, time))
    f.sort()
    return(f)

def get_persistence( simplices: List[List]) -> Any:
    """
    Feed Delaunay triangulation in, get persistence diagram
    Forward sort since this is function d

    Args:
        simplices: list of simplicial complexes
    Return:
        dgms: persistence birth, death tuples (encoded in)
    """
    import dionysus as d
    f = d.Filtration()
    for vertices, time in simplices:
        f.append(d.Simplex(vertices, time))
    f.sort()
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)
    return(dgms)

def is_simplicial(f : Any) -> None:
    """
    Debugger function to see where edge is missing
    Arg:
        f: filtration
    """

    for s in f:
        if len(s) != len(set(s)):
            print("%s is not a simplex" % s)
        for sb in s.boundary():
            if sb not in f:
                print("%s in boundary of %s not found in the filtration" % (sb, s))

if __name__=="__main__":
    print(filepaths)
    xyz_file = filepaths[0]
    print(xyz_file)
    print(type(xyz_file))
    latticeCsts = lattice_param(filepaths[0])
    #create 100x100x100 cell
    newCell = copies_to_fill_cell(90, filepaths[0], latticeCsts)
    simplices = get_delaunay_simplices(newCell)
    dgms = get_persistence(simplices)
    print(dgms)
