import pydicom
import numpy as np
from PIL import Image


def convert_pillow_image1(dicom_array):
    float_dicom_array = dicom_array.astype(np.float32)
    positive_dicom_array = np.maximum(float_dicom_array, 0)
    normalized_dicom_array = positive_dicom_array / positive_dicom_array.max()
    normalized_dicom_array *= 255
    uint8_image = np.uint8(normalized_dicom_array)

    pillow_image = Image.fromarray(uint8_image)

    return pillow_image


def convert_pillow_image2(dicom_array):
    hounsfield_min = np.min(dicom_array)
    hounsfield_max = np.max(dicom_array)
    hounsfield_range = hounsfield_max - hounsfield_min

    dicom_array[dicom_array < hounsfield_min] = hounsfield_min
    dicom_array[dicom_array > hounsfield_max] = hounsfield_max

    normalized_array = (dicom_array - hounsfield_min) / hounsfield_range
    normalized_array *= 255
    uint8_image = np.uint8(normalized_array)

    pillow_image = Image.fromarray(uint8_image)


    return pillow_image


if __name__ == "__main__":
    dicom_file = pydicom.dcmread("data/CT/1-01.dcm")

    # print(dicom_file)
    # print(dicom_file.PatientName)
    # print(dicom_file.PatientID)
    # print(dicom_file.SOPInstanceUID)
    # print(dicom_file.pixel_array.shape)

    dicom_array = dicom_file.pixel_array

    pillow_image1 = convert_pillow_image1(dicom_array)
    pillow_image1.show()

    pillow_image2 = convert_pillow_image2(dicom_array)
    pillow_image2.show()