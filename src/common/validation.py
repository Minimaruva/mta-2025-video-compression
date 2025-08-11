import os.path
import os
from src.common import dataset
from src.common import GLOBAL_VARIABLES
import subprocess
from PIL import Image
import numpy as np

class Validation(dataset.Dataset):
    filepath = None
    folders = []

    def prepare_dataset(self,
                        filepath_sequences: str = "originals",
                        dataset_path: str = "dataset",
                        clean_reinstall: bool = False):
        
        #Check if folder exist
        if (not os.path.exists(filepath_sequences)):
            RuntimeError(f"{filepath_sequences} doesn't exist")
        if (not os.path.exists(dataset_path)):
            os.makedirs(dataset_path)
        
        self.filepath_sequences = filepath_sequences
        self.dataset_path = dataset_path
        self.folders = []
        
        #Prepare dataset
        if (not os.path.exists(os.path.join(dataset_path, "cleaned"))):
            os.makedirs(os.path.join(dataset_path, "cleaned"))
        
        for sequence in os.listdir(filepath_sequences):
            filename_base = os.path.basename(sequence)
            filename_base_no_extension = os.path.splitext(filename_base)[0]
            filename = os.path.join(filepath_sequences, filename_base)
            self.folders.append(os.path.join(dataset_path, "cleaned", filename_base_no_extension))

            if (not os.path.exists(os.path.join(dataset_path, "cleaned", filename_base_no_extension))):
                os.makedirs(os.path.join(dataset_path, "cleaned", filename_base_no_extension))
            elif not clean_reinstall:
                continue
            command = [
                "ffmpeg",
                "-i", filename,
                "-vf", f"crop={GLOBAL_VARIABLES.WIDTH}:{GLOBAL_VARIABLES.HEIGHT}:0:0",
                "-pix_fmt", "yuv420p",
                os.path.splitext(os.path.join(dataset_path, "cleaned", filename_base_no_extension, filename_base))[0] + "_%06d.png"]

            subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    def max(self, folder: str):
        return len(self.files(folder))
    
    def files(self, folder: str, sorted=False):
        files_list = [name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]
        if sorted:
            files_list.sort()
        return [os.path.join(folder, filename) for filename in files_list]

    def load(self, folder: str, id: int):
        if id >= self.max(folder):
            RuntimeWarning("ID index is bigger than number of frames")
        filename_id = os.path.join(folder, (os.listdir(os.path.join(folder)))[id])
        return np.asarray(Image.open(filename_id)), filename_id