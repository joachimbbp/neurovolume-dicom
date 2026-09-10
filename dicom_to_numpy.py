from pathlib import Path
import pydicom
import numpy as np
# load the DICOM files
def load_slices(dicom_dir: Path, enforce_dcm = False):
    files = []
    for fname in dicom_dir.iterdir():
      if fname.is_file():
          if enforce_dcm:
              assert fname.suffix == ".dcm"
          print(f"loading: {fname}")
          files.append(pydicom.dcmread(fname, force=(not enforce_dcm)))
    print(f"file count: {len(files)}")
    return files

def slices_to_np(files) -> np.ndarray:
    # skip files with no SliceLocation (eg scout views)
    slices = []
    skipcount = 0
    for f in files:
      if hasattr(f, "SliceLocation"):
          slices.append(f)
      else:
          skipcount = skipcount + 1

    print(f"skipped, no SliceLocation: {skipcount}")

    # ensure they are in the correct order
    slices = sorted(slices, key=lambda s: s.SliceLocation)
    
    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
      img2d = s.pixel_array
      img3d[:, :, i] = img2d
    return img3d
