from pathlib import Path
import pydicom
import numpy as np
import matplotlib.pyplot as plt
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

def slices_to_np(files, plot=False):
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

    # pixel aspects, assuming all slices are the same
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1] / ps[0]
    sag_aspect = ps[1] / ss
    cor_aspect = ss / ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
      img2d = s.pixel_array
      img3d[:, :, i] = img2d

    if plot:
        # plot 3 orthogonal slices
        a1 = plt.subplot(2, 2, 1)
        plt.imshow(img3d[:, :, img_shape[2] // 2])
        a1.set_aspect(ax_aspect)

        a2 = plt.subplot(2, 2, 2)
        plt.imshow(img3d[:, img_shape[1] // 2, :])
        a2.set_aspect(sag_aspect)

        a3 = plt.subplot(2, 2, 3)
        plt.imshow(img3d[img_shape[0] // 2, :, :].T)
        a3.set_aspect(cor_aspect)

        plt.show()

    return img3d
