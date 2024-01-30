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


def anonymize_dicom(
    dcm_file: str,
    patient_name: str | None = None,
    patient_birthdate: str | None = None,
    patient_sex: str | None = None,
    study_id: str | None = None,
    save_path: str | None = None,
) -> pydicom.Dataset:
    """anonymize DICOM file

    Args:
        dcm_file (str): DICOM file path
        patient_name (str | None, optional): patient name. Defaults to None.
        patient_birthdate (str | None, optional): patient birth date. Defaults to None.
        patient_sex (str | None, optional): patient sex. Defaults to None.
        study_id (str | None, optional): study ID. Defaults to None.
        save_path (str | None, optional): save path. Defaults to None.

    Returns:
        pydicom.Dataset: anonymized DICOM file
    """
    dicom_file = pydicom.dcmread(dcm_file)

    if patient_name:
        dicom_file.PatientName = patient_name
    else:
        dicom_file.PatientName = ""

    if patient_birthdate:
        dicom_file.PatientBirthDate = patient_birthdate
    else:
        dicom_file.PatientBirthDate = ""

    if patient_sex:
        dicom_file.PatientSex = patient_sex
    else:
        dicom_file.PatientSex = ""

    if study_id:
        dicom_file.StudyID = study_id
    else:
        dicom_file.StudyID = ""

    if save_path:
        dicom_file.save_as(save_path)

    return dicom_file


def change_tags(dcm_file, **kwargs) -> pydicom.Dataset:
    """change tags of DICOM file

    Args:
        dcm_file (str): DICOM file path
        **kwargs: DICOM tags

    Returns:
        pydicom.Dataset: DICOM file
    """
    dicom_file_data = pydicom.dcmread(dcm_file)

    for key, value in kwargs.items():
        if value is None:
            continue

        if key in dicom_file_data:
            setattr(dicom_file_data, key, value)

    return dicom_file_data


if __name__ == "__main__":
    normalize_visualize_dicom_1("data/CT/1-01.dcm", show=True)
    normalize_visualize_dicom_2(
        "data/CT/1-01.dcm", max_value=200, min_value=-200, show=True
    )
