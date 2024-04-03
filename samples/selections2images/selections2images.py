""" selections2images.py
=============
Sample script for Client.selections2images. """

from __future__ import annotations
from tropy_utility.client import Client
import os.path


DIR = os.path.dirname(__file__)

Client().selections2images(tropy_file_path=f"{DIR}/tropy_project.json",
                           images_dir=DIR,
                           selections_dir=DIR)
