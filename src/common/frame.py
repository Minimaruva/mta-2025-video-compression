import numpy as np
from PIL import Image
import shutil
import os
import json
import dataclasses

from src.common.metadata import Metadata

class Frame:
    image: np.array = None
    metadata: Metadata

    def __init__(self, filename: str, json_folder=None):
        self.image = np.asarray(Image.open(filename))
        if json_folder is not None:
            shutil.copyfile(os.path.join(json_folder, os.path.basename(os.path.splitext(filename)[0] + ".json")),
                            os.path.splitext(filename)[0] + ".json")
        if os.path.isfile(os.path.splitext(filename)[0] + ".json"):
            with open(os.path.splitext(filename)[0] + ".json") as f:
                json_load = json.load(f)
                self.metadata = Metadata()
                self.metadata.offset = json_load["offset"]
                self.metadata.scale = json_load["scale"]
        else:
            self.metadata = Metadata()
    
    def load(self):
        return self.image
    
    def save(self, folder: str, id: int) -> str:
        if (not os.path.exists(folder)):
            os.makedirs(folder)
        Image.fromarray(self.image).save(os.path.join(folder, str(id+1).zfill(6) + ".png")) #+1 for ID to align with ffmpeg
        with open(os.path.join(folder,  str(id+1).zfill(6) + ".json"), "w") as f:
            json.dump(dataclasses.asdict(self.metadata), f)
        return os.path.join(folder, str(id+1).zfill(6) + ".png")