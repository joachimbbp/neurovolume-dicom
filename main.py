import numpy as np
import neurovolume as nv
from pathlib import Path
import dicom_to_numpy

def main():
    # download your own sample from https://saga-it.com/dicom/samples
    dicom_series = Path("./ct-chest-lidc-idri-series")
    dicom_slices = dicom_to_numpy.load_slices(dicom_series)
    dicom_ndarray = dicom_to_numpy.slices_to_np(dicom_slices)
    prepped_np = nv.prep_ndarray(dicom_ndarray)
    # HINT: if srambled, try changing the cartesian_order
    chest_grid = nv.Grid("chest", prepped_np)
    # Note to self: it would be nice if .write() took the SaveConfig and had optional loudness
    chest_volume = nv.Volume([chest_grid], save_config=nv.SaveConfig("chest", folder=Path("./output")))
    chest_volume.write()

if __name__ == "__main__":
    main()
