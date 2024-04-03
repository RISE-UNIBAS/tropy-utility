""" client.py
=============
Client class. """

from __future__ import annotations

import os.path
import shutil
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

        logging.info(f"--->Starting Client.selections2images...")

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
                        selection_image = image.crop((selection["x"], selection["y"],
                                                      selection["x"] + selection["width"],
                                                      selection["y"] + selection["height"]))
                        selection_image_name = f"{image_name.split('.')[0]}_selection_{index}.{image_name.split('.')[-1]}"
                        selection_image.save(fp=f"{selections_dir}/{selection_image_name}")
                        logging.info(f"{item['title']}: {selection_image_name} saved to {selections_dir}.")
            except KeyError:
                logging.exception(f"Something went wrong with {item['title']}.")
            except Exception as e:
                raise e

        logging.info(f"<---Client.selections2images finished.")

    def items2transkribus(self,
                          tropy_file_path: str,
                          images_dir: str,
                          transkribus_dir: str,
                          flag: str = None) -> None:
        """ Create a folder for each Tropy item that can be ingested into Transkribus.

        The aim is to have one Transkribus document per Tropy item. Ingest the folders with the Transkribus FTP Client.
        Folder resp. document names are item titles (if any).

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param images_dir: the input directory of the images corresponding to the Tropy export
        :param transkribus_dir: the target directory of the Transkribus export
        :param flag: only items with this tag will be processed, defaults to None
        """

        logging.info(f"--->Starting Client.items2transkribus...")

        tropy = self._load_tropy_input(tropy_file_path=tropy_file_path)

        for index, item in enumerate(tropy["@graph"]):
            if flag is not None:
                try:
                    if flag not in item["tag"]:
                        continue
                except KeyError:
                    continue

            # make item folder in transkribus_dir:
            try:
                item_name = item["title"]
            except KeyError:
                logging.error(f"Error: Item number {index + 1} does not have a title!")
                item_name = f"item_number_{index + 1}"
            item_dir = f"{transkribus_dir}/{item_name}"
            try:
                os.mkdir(path=item_dir)
            except FileExistsError:
                logging.error(f"Error: Item number {index + 1} does not have a unique title!")
                item_dir = f"{transkribus_dir}/item_number_{index + 1}"
                os.mkdir(path=item_dir)

            # copy item images to this folder:
            for photo in item["photo"]:
                photo_name = photo["filename"]
                try:
                    shutil.copy(src=f"{images_dir}/{photo_name}",
                                dst=item_dir)
                except Exception as e:
                    logging.error(e)

            # TODO: write item metadata to XML (specs required)

            logging.info(f"Exported item number {index + 1} successfully to {item_dir}.")

        logging.info(f"<---Client.items2transkribus finished.")
