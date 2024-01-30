"""DICOM handler"""

import pydicom
import numpy as np
from PIL import Image


def normalize_visualize_dicom_1(dcm_file: str, show: bool = True) -> np.uint8:
    """normalize and visualize dicom image

    Args:
        dcm_file (str): DICOM file path
        show (bool, optional): whether to show the image. Defaults to True.

    Returns:
        np.uint8: normalized image
    """
    dicom_file = pydicom.dcmread(dcm_file)
    dicom_array = dicom_file.pixel_array.astype(np.float32)
    normalized_dicom_array = ((np.maximum(dicom_array, 0)) / dicom_array.max()) * 255.0
    uint8_image = np.uint8(normalized_dicom_array)

    if show:
        pillow_image = Image.fromarray(uint8_image)
        pillow_image.show()

    return uint8_image


def normalize_visualize_dicom_2(
    dcm_file: str,
    max_value: int | None = None,
    min_value: int | None = None,
    show: bool = True,
) -> np.uint8:
    """normalize and visualize dicom image

    Args:
        dcm_file (str): DICOM file path
        max_value (int | None, optional): houns field max value. Defaults to None.
        min_value (int | None, optional): houns field minimum value. Defaults to None.
        show (bool, optional): whether to show the image. Defaults to True.

    Returns:
        np.uint8: normalized image
    """
    dicom_dile = pydicom.dcmread(dcm_file)
    dicom_array = dicom_dile.pixel_array

    if max_value:
        hounsfield_max = max_value
    else:
        hounsfield_max = np.max(dicom_array)

    if min_value:
        hounsfield_min = min_value
    else:
        hounsfield_min = np.min(dicom_array)

    hounsfield_range = hounsfield_max - hounsfield_min

    dicom_array[dicom_array < hounsfield_min] = hounsfield_min
    dicom_array[dicom_array > hounsfield_max] = hounsfield_max

    normalized_array = ((dicom_array - hounsfield_min) / hounsfield_range) * 255.0
    uint8_image = np.uint8(normalized_array)

    if show:
        pillow_image = Image.fromarray(uint8_image)
        pillow_image.show()

    return uint8_image


if __name__ == "__main__":
    normalize_visualize_dicom_1("data/CT/1-01.dcm", show=True)
    normalize_visualize_dicom_2(
        "data/CT/1-01.dcm", max_value=200, min_value=-200, show=True
    )
