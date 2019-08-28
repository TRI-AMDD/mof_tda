"""
This module is intended to facilitate the ingestion of json documents
harvested from the MOFDB database into a docdb, whether mongo
or AWS DocDB
"""
import json
import boto3
import os

from pymongo import MongoClient
from monty.serialization import loadfn
from mof_tda import MOF_TDA_PATH


# Specify MOF_TDA_DB_MODE as "local" or "aws"
MOF_TDA_DB_MODE = os.environ.get("MOF_TDA_DB_MODE", "local")


def get_config():
    """
    Retrieves db configuration from AWS secrets manager

    Returns:
        (dict): dictionary of keys and values associated
            with AWS DocDB

    """
    if MOF_TDA_DB_MODE.lower() == "aws":
        secret_name = "stage/mof_tda/db/main"
        client = boto3.client("secretsmanager")
        secret = client.get_secret_value(SecretId=secret_name)
        return json.loads(secret['SecretString'])

    elif MOF_TDA_DB_MODE.lower() == "local":
        return {"hostname": "localhost",
                "port": 27017,
                "username": None,
                "password": None}


def get_db():
    """
    Gets mongo database object associated with mof tda and
    prescribed database mode

    Returns:


    """
    config = get_config()
    client = MongoClient(**config)
    return client["mof_tda"]


def add_isotherms_to_database(filename=None):
    """
    Adds isotherm documents to database

    Returns:
        None

    """
    filename = filename or os.path.join(
        MOF_TDA_PATH, "ingest", "mofdb_isotherms",
        "mofdb_isotherms_structure.json")

    data = loadfn(filename)
    db = get_db()
    db.insert_many(data)


if __name__ == "__main__":
    add_isotherms_to_database()
