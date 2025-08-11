from skimage import metrics
import math
from src.common.frame import Frame
import os

class Metrics:
    references = None
    tests = None
    def __init__(self, anchor, test):
        self.anchor_dir = anchor
        self.anchor = os.listdir(anchor)
        self.anchor = [i for i in self.anchor if "png" in i]
        self.anchor.sort()

        self.test_dir = test
        self.test = os.listdir(test)
        self.test = [i for i in self.test if "png" in i]
        self.test.sort()

    def PSNR_one_frame(self, ref_frame: Frame, test_frame: Frame):   
        """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
        res = metrics.peak_signal_noise_ratio(ref_frame.image, test_frame.image)
        if math.isinf(res):
            return 100
        else:
            return res
        
    def PSNR(self):
        total, number = 0, 0
        for anchor, test in zip(self.anchor, self.test):
            anchor, test = Frame(os.path.join(self.anchor_dir, anchor)), Frame(os.path.join(self.test_dir, test))
            total += self.PSNR_one_frame(anchor, test)
            number += 1
        return total/number
            