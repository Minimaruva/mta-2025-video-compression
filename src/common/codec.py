import subprocess
import os
import ffmpeg

def get_bitrate(file):
    try:
        probe = ffmpeg.probe(file)
        size = probe["format"]["size"]
        kilo_size= float(float(size) / 1000)
        return kilo_size
    except:
        RuntimeError("Couldn't get bitrate")
class Codec:
    codec = None
    def __init__(self, qp, codec="265"):
        if codec not in ["265"]:
            NotImplementedError(f"Codec {codec} not implemented")
        
        self.qp = qp
        self.codec = codec
        
    def encode(self, folder_name: str, output_folder: str):
        if (not os.path.exists(output_folder)):
            os.makedirs(output_folder)
        #png to 265
        command = ["ffmpeg", "-framerate", "30", "-i", os.path.join(folder_name, "%06d.png")]
        command += ["-r", "30", \
            "-c:v", "libx265", \
            "-x265-params", f"qp={self.qp}:p=veryfast", \
            os.path.join(output_folder, "tmp.265")]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        bitrate = get_bitrate(os.path.join(output_folder, "tmp.265"))
        
        #265 back to png
        command = ["ffmpeg", \
            "-i", os.path.join(output_folder, "tmp.265"), \
            os.path.join(output_folder, "%06d.png")
        ]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(os.path.join(output_folder, "tmp.265"))
        return bitrate