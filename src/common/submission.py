import os.path
from src.preprocess import preprocess_script
from src.postprocess import postprocess_script
from src.common.metrics import Metrics
from src.common.frame import Frame
from src.common.codec import Codec
from src.common.GLOBAL_VARIABLES import *
import bjontegaard as bd
import sys

from src.common.common import delete_folder

def get_sizeof_dataclass(dataclass_instance):
    """
    Calculates the size (in bytes) of a dataclass instance in memory.

    Args:
    dataclass_instance: An instance of a dataclass.

    Returns:
    The size of the dataclass instance in bytes.
    """

    size = sys.getsizeof(dataclass_instance)  # Initial size (including overhead)

    # Iterate through fields to account for their sizes.  This part is crucial
    # because sys.getsizeof() often doesn't accurately reflect the total size,
    # # especially for nested objects or mutable types.
    for field in dataclass_instance.__dataclass_fields__.values():
        field_value = getattr(dataclass_instance, field.name)

    if field.type is list:
        # Special handling for lists.  Calculate size of each element and the list overhead.
        size += len(field_value) * sys.getsizeof(field_value[0]) if field_value else 0  # Size of elements
        size += sys.getsizeof([]) # Add list overhead.
    elif field.type is dict:
    #Special handling for dicts
        size += sys.getsizeof({}) #Dict overhead
        for key, value in field_value.items():
            size += sys.getsizeof(key)
            size += sys.getsizeof(value)
    else:
        # Add the size of the field value
        size += sys.getsizeof(field_value)

    return size

def bench_submission(folder, qp, is_anchor=True):
    input_folder = os.path.join(CLEANED_DATA_FOLDER, folder)
    preprocess_folder = os.path.join(PREPROCESS_DATA_FOLDER, folder)
    encoded_folder = os.path.join(ENCODED_DATA_FOLDER, folder)
    postprocess_folder = os.path.join(POSTPROCESS_DATA_FOLDER, folder)
    delete_folder(preprocess_folder)
    delete_folder(postprocess_folder)
    delete_folder(encoded_folder)
    
    imgs = []
    ordered_input_folder = os.listdir(input_folder)
    ordered_input_folder.sort()
    bitrate = 0
    for index, file in enumerate(ordered_input_folder):
        original_img = Frame(os.path.join(input_folder, file))
        if is_anchor:
            imgs.append(original_img.save(preprocess_folder, index))
        else:
            img = preprocess_script.preprocess(original_img)
            bitrate += get_sizeof_dataclass(img.metadata) * 8 / 1000
            imgs.append(img.save(preprocess_folder, index))
    bitrate /= (30)
    
    codec = Codec(qp)
    bitrate += codec.encode(preprocess_folder, encoded_folder)
    imgs = []
    ordered_encoded_folder = os.listdir(encoded_folder)
    ordered_encoded_folder.sort()
    for index, file in enumerate(ordered_encoded_folder):
        original_img = Frame(os.path.join(encoded_folder, file), preprocess_folder)
        if is_anchor:
            imgs.append(original_img.save(postprocess_folder, index))
        else:
            img = postprocess_script.postprocess(original_img)
            imgs.append(img.save(postprocess_folder, index))

    metric = Metrics(input_folder, postprocess_folder)
    return [bitrate, metric.PSNR()]
    
def folder_submission(folder, return_dict):
    bitrates_anchor = []
    psnrs_anchor = []
    bitrates_test = []
    psnrs_test = []
    for qp in QPS:
        bitrate, psnr = bench_submission(folder, qp, is_anchor=True)
        bitrates_anchor.append(bitrate)
        psnrs_anchor.append(psnr)

        bitrate, psnr = bench_submission(folder, qp, is_anchor=False)  # <-- FIXED To false here
        bitrates_test.append(bitrate)
        psnrs_test.append(psnr)
    try:
        return_dict[folder] = bd.bd_rate(bitrates_anchor, psnrs_anchor, bitrates_test, psnrs_test, method='akima')
    ## Changed this part of original code
    except Exception as e:
        print(f"Error in BD-rate calculation for {folder}: {e}")
        return_dict[folder] = -77777