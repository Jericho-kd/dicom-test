import numpy as np
from pathlib import Path
from pydicom import dcmread, Dataset


def rotate_image_90_degrees(out_dir: Path) -> None:
    for dcm_file in Path(out_dir).glob("*.dcm"):
        dataset: Dataset = dcmread(dcm_file)

        rotated_array = np.rot90(dataset.pixel_array)
        dataset.PixelData = rotated_array.tobytes()
        dataset.Rows, dataset.Columns = rotated_array.shape

        tmp_s_uid = dataset.SeriesInstanceUID.split('.')
        tmp_s_uid[-1] = str(int(tmp_s_uid[-1]) + 1)
        dataset.SeriesInstanceUID = '.'.join(tmp_s_uid)

        dataset.save_as(dcm_file)