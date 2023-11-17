""" client.py
=============
Client class. """

from __future__ import annotations
from dataclasses import dataclass
from PIL import Image
from tropy_utility.utility import Utility
import json
import logging
import time


@dataclass
class Client:
    """ Standalone client. """

    def __post_init__(self):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                            handlers=[logging.FileHandler(f"tropy_utility_{time.strftime('%Y%m%d-%H%M%S')}.log"),
                                      logging.StreamHandler(),
                                      ]
                            )
        logging.info(f"Started Client.")

    @staticmethod
    def _load_tropy_input(tropy_file_path: str) -> dict:
        """ Load Tropy project file input.

        :param tropy_file_path: complete path to Tropy export file including file extension
        """

        try:
            return Utility.load_json(file_path=tropy_file_path)
        except FileNotFoundError:
            logging.critical(f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' not found!")
            raise
        except json.JSONDecodeError:
            logging.critical(
                f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' is not a valid Tropy export file!")
            raise

    def selections2images(self,
                          tropy_file_path: str,
                          images_dir: str,
                          selections_dir: str,
                          flag: str = None) -> None:
        """ Save all selections of all images of a Tropy project as new images.

        For an item with image i, the selection j will be saved as image_i_selection_j. Select a subset of items via
        the flag parameter.

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param images_dir: the directory of the images corresponding to the Tropy export
        :param selections_dir: the directory where the selections are to be saved
        :param flag: only images of items with this tag will be processed, defaults to None
        """

        tropy = self._load_tropy_input(tropy_file_path=tropy_file_path)

        for item in tropy["@graph"]:
            if flag is not None:
                try:
                    if flag not in item["tag"]:
                        continue
                except KeyError:
                    continue
            try:
                for photo in item["photo"]:
                    image_name = photo["filename"]
                    for index, selection in enumerate(photo["selection"], start=1):
                        image = Image.open(f"{images_dir}/{image_name}")
                        selection_image = image.crop((selection["x"], selection["y"], selection["x"] + selection["width"], selection["y"] + selection["height"]))
                        selection_image_name = f"{image_name.split('.')[0]}_selection_{index}.{image_name.split('.')[-1]}"
                        selection_image.save(fp=f"{selections_dir}/{selection_image_name}")
                        logging.info(f"{item['title']}: {selection_image_name} saved to {selections_dir}.")
            except KeyError:
                logging.exception(f"Something went wrong with {item['title']}.")
            except Exception as e:
                raise e
