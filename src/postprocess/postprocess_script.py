from src.common.frame import Frame
import numpy as np

def postprocess(input_img: Frame):
    #FIXME
    # You can do postprocessing here
    input_img.image = np.where(input_img.image != 255, input_img.image + input_img.metadata.offset, 255)
    
    #check that values are still correct
    input_img.image = np.clip(input_img.image, 0, 255)
    return input_img

def main(input_img):
    print("Starting decoder script")
    NotImplementedError()
    
if __name__ == "__main__":
    main()