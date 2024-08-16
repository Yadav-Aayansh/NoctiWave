# /NoctiWave/run.py

from app import database_creator
from app import app_creator

if __name__ == "__main__":
    database_creator()
    app_creator()
