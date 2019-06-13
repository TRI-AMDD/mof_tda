import numpy as np
import hashlib #debugging
from typing import (Any, Set, List, Tuple, Dict, Optional, TextIO)
import dionysus as d
import diode
from createCubicCells import copiesToFillCell, latticeParam

mof_files = 'subset_mof_list.txt'
filepaths = []
with open(mof_files,'r') as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4] #strip .cif off
        filepaths.append(stripped_line + ".xyz")

def getDelaunaySimplices(points : List[List]) -> List[List]:
    simplices = diode.fill_alpha_shapes(points)
    return simplices

def getFiltration( simplices : List[List]) -> Any:
    f = d.Filtration()
    for vertices, time in simplices:
        f.append(d.Simplex(vertices, time))
    f.sort()
    return(f)

def getPersistence( simplices: List[List]) -> Any:
    #Feed Delaunay triangulation in, get persistence diagram
    #Forward sort since this is function d
    import dionysus as d
    f = d.Filtration()
    for vertices, time in simplices:
        f.append(d.Simplex(vertices, time))
    f.sort()
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)
    return(dgms)

def is_simplicial(f : Any) -> None:
    """ Debugging to see where edge is missing """
    for s in f:
        if len(s) != len(set(s)):
            print("%s is not a simplex" % s)
        for sb in s.boundary():
            if sb not in f:
                print("%s in boundary of %s not found in the filtration" % (sb, s))

if __name__=="__main__":
    xyz_file = filepaths[0]
    print(type(xyz_file))
    latticeCsts = latticeParam(filepaths[0])
    #create 100x100x100 cell
    newCell = copiesToFillCell(90, latticeCsts, filepaths[0])
    simplices = getDelaunaySimplices(newCell)
    dgms = getPersistence(simplices)
    print(dgms)
