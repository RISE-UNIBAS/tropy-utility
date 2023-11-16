""" client.py
=============
Client class. """

from __future__ import annotations
from dataclasses import dataclass
from PIL import Image
from tropy_utility.utility import Utility
import json
import logging
import os.path
import time

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE = f"{PARENT_DIR}/sample"
DATA = f"{PARENT_DIR}/data"
TESTS = f"{PARENT_DIR}/tests"


@dataclass
class Client:
    """ Standalone client. """

    def __post_init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                            handlers=[logging.FileHandler(f"tropy_utility_{time.strftime('%Y%m%d-%H%M%S')}.log"),
                                      logging.StreamHandler(),
                                      ]
                            )
        logging.info(f"Started Client.")

    @staticmethod
    def selections2images(tropy_file_path: str,
                          images_dir: str,
                          selections_dir: str,
                          flag: str = None) -> None:
        """ Save all selections of all images of a Tropy project as new images.

        For an item with image i, the selection j will be saved as image_i_selection_j.

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param images_dir: the directory of the images corresponding to the Tropy export
        :param selections_dir: the directory where the selections are to be saved
        :param flag:
        """

        try:
            tropy = Utility.load_json(file_path=tropy_file_path)
        except FileNotFoundError:
            logging.critical(f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' not found!")
            raise
        except json.JSONDecodeError:
            logging.critical(
                f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' is not a valid Tropy export file!")
            raise

        for item in tropy["@graph"]:
            if flag is not None:
                pass  # TODO: implement flag via tag
            try:
                for photo in item["photo"]:
                    selection_counter = 1
                    image_name = photo["path"].split("\\")[-1]

                    for selection in photo["selection"]:
                        x = selection["x"]
                        y = selection["y"]
                        w = selection["width"]
                        h = selection["height"]
                        image = Image.open(f"{images_dir}/{image_name}")
                        selection_image = image.crop((x, y, x + w, y + h))
                        selection_image_name = f"{image_name.split('.')[0]}_selection_{selection_counter}.{image_name.split('.')[-1]}"
                        selection_image.save(fp=f"{selections_dir}/{selection_image_name}")
                        selection_counter += 1
                        logging.info(f"{item['title']}'s {selection_image_name} saved to {selections_dir}.")
            except Exception as e:
                raise e


Client().selections2images(tropy_file_path=f"{SAMPLE}/tropy_project.json",
                           images_dir=SAMPLE,
                           selections_dir=SAMPLE)