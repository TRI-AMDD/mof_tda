"""
This module contains functionality for the ingestion of data from the MOF DB
hosted by the Snurr research lab at Northwestern University.  Note that
none of this code is based on any explicit documentation of the MOF DB,
but on inferences from inspection of the frontend code and query parameters.

As such, future iterations may need refactoring if the API changes.

The MOF DB frontend is hosted at https://mof.tech.northwestern.edu
"""
import requests
import json
from tqdm import tqdm
from multiprocessing import Pool
from monty.serialization import dumpfn, loadfn
from monty.shutil import compress_file
from mof_tda import MOF_TDA_PATH, MOF_TDA_CIF_PATH
import os


MOFDB_URL = "https://mof.tech.northwestern.edu"


def fetch_mofdb_cif(mof_name):
    """
    Fetches MOFDB structure according to name key

    Args:
        mof_name (string): string corresponding to MOF name, e.g.
            FECWOB_clean

    Returns:
        cif string corresponding to mof

    """
    url = "{}/cifs/{}.cif".format(MOFDB_URL, mof_name)
    response = requests.get(url)
    return response.content.decode()


def fetch_mofdb_isotherm(iso_id):
    """
    Fetches a json document from the MOFDB API for an isotherm
    for a given structure

    Args:
        iso_id (int): id for query parameter in URL

    Returns:
        (dict) document corresponding to fetched json from server

    """
    response = requests.get("{}/iso.php?id={}".format(MOFDB_URL, iso_id))
    return json.loads(response.content)


def fetch_many_docs(iso_ids, nproc=1):
    """

    Args:
        iso_ids ([int]): list of iso_ids to fetch
        nproc (int): number of processes to use, if greater than 1, will use
            larger number of processes

    Returns:
        ([dict]) list of fetched documents

    """
    if nproc > 1:
        with Pool(nproc) as pool:
            return list(tqdm(pool.imap(fetch_mofdb_isotherm, iso_ids),
                             total=len(iso_ids)))
        pass
    else:
        return [fetch_mofdb_isotherm(iso_id) for iso_id in tqdm(iso_ids)]


# TODO: Could fetch cifs and isotherms together, refactor
#       if we end up having to do another big ingestion
def fetch_preset(output_filename=None, nproc=8, add_structure=True):
    """
    Fetches preset list of docs determined via trial and error,

    An initial query via the frontend on 06/28/2019 showed 12870,
    and subsequent sampling of ids from 8000-25000 yielded all 12820.
    Successful query ids were stored in indices.json, up which this
    function should be able extract all of the relevant data.

    Args:
        output_filename (str): output filename for all collected docs
        nproc (int): number of processes to use

    Returns:
        (List): list of isotherm documents
    """
    # Load indices from json doc
    iso_ids = loadfn(os.path.join(MOF_TDA_PATH, "ingest", "indices.json"))

    # Fetch all docs from ids
    isotherms = fetch_many_docs(iso_ids, nproc=nproc)

    # Dump to json if output specified
    if output_filename is not None:
        dumpfn(isotherms, output_filename)
    return isotherms


def add_structures(isotherms):
    """

    Args:
        isotherms (List): list of isotherm docs, e. g. from
            fetch_many_docs

    Returns:
        (List): isotherm data with structures added

    """
    for isotherm in tqdm(isotherms):
        # Get structure name/filename
        mof_name = isotherm['adsorbent']['name']
        structure_filename = os.path.join(
            MOF_TDA_CIF_PATH, "{}.cif".format(mof_name))
        # Read in and add structure cif string if present
        if os.path.isfile(structure_filename):
            with open(structure_filename) as f:
                cif_string = f.read()
        # If not present, fetch it from db
        else:
            cif_string = fetch_mofdb_cif(mof_name)

        isotherm['adsorbent']['cif'] = cif_string
    return isotherms


if __name__ == "__main__":
    # Initial scraping
    fname = os.path.join(MOF_TDA_PATH, "ingest", "mofdb_isotherms.json")
    if not os.path.isfile(fname):
        isotherms = fetch_preset(fname)
    else:
        isotherms = loadfn(fname)

    # Postprocessing with structure add
    isotherms = add_structures(isotherms)
    dumpfn(isotherms, "mofdb_isotherms_structure.json")
    compress_file("mofdb_isotherms_structure.json")

