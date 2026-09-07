from pathlib import Path
import dicom_to_numpy

def main():
    # download your own sample from https://saga-it.com/dicom/samples
    dicom_series = Path("./ct-chest-lidc-idri-series")

    slices = dicom_to_numpy.load_slices(dicom_series)
    np = dicom_to_numpy.slices_to_np(slices, True)

if __name__ == "__main__":
    main()
