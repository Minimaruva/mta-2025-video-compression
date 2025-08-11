from src.common.frame import Frame
import numpy as np

def preprocess(input_img: Frame):
    #FIXME
    input_img.metadata.scale = int(np.max(input_img.image))
    # You can modify Metadata that can be sent here
    input_img.metadata.offset = 1
    # You can also do preprocessing
    input_img.image = np.where(input_img.image != 0, input_img.image - input_img.metadata.offset, 0)
    
    #check that values are still correct
    input_img.image = np.clip(input_img.image, 0, 255)
    return input_img

def main(input_img):
    print("Starting encoder script")
    NotImplementedError()
    
if __name__ == "__main__":
    main()