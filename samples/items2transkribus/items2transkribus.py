""" items2transkribus.py
=============
Sample script for Client.items2transkribus.py. """

from __future__ import annotations
from tropy_utility.client import Client
import os.path


DIR = os.path.dirname(__file__)

Client().items2transkribus(tropy_file_path=f"{DIR}/tropy_project.json",
                           images_dir=DIR,
                           transkribus_dir=DIR)
