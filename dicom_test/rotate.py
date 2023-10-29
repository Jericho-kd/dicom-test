import numpy as np
from pathlib import Path
from pydicom import dcmread, Dataset


def image_rotate(out_dir: Path) -> None:
    for dcm_file in Path(out_dir).glob("*.dcm"):
        dataset: Dataset = dcmread(dcm_file)

        rotated_array = np.rot90(dataset.pixel_array)
        dataset.PixelData = rotated_array.tobytes()
        dataset.Rows, dataset.Columns = rotated_array.shape

        tmp_sop = dataset.SeriesInstanceUID.split('.')
        tmp_sop[-1] = str(int(tmp_sop[-1]) + 1)
        dataset.SeriesInstanceUID = '.'.join(tmp_sop)

        dataset.save_as(dcm_file)
        