import numpy as np
import imageio
import math

# Normalizes a given image in a pixel value range from 0 to max
def normalizeRange(original: np.ndarray, max: int, pixelType: type) -> np.ndarray:
    return ((original - np.min(original)) / (np.max(original) - np.min(original)) * max).astype(pixelType)

# Calculates the RMSE of the comparison between two images
def RMSE(ref: np.ndarray, result: np.ndarray) -> float:
    sums = 0
    for i, row in enumerate(ref):
        for j, pixel in enumerate(row):
            sums += (pixel - float(result[i][j])) ** 2
    return math.sqrt(sums / (len(ref) * len(ref[0])))

# Loading input images
filenameI = str(input()).rstrip()
img = imageio.imread(filenameI)
filenameM = str(input()).rstrip()
fltr = imageio.imread(filenameM)
filenameG = str(input()).rstrip()
reference = imageio.imread(filenameG)

# Generating the Fourier Spectrum of the input image
spectrum = np.fft.fft2(img)

# Shifts the lower frequencies to the middle of the spectrum
# Applies the filter to the spectrum
# Reverts the shifting to return to the original arrangement
filteredSpectrum = np.fft.ifftshift(np.fft.fftshift(spectrum) * normalizeRange(fltr, 1, np.uint8))

# Generates the filtered image back into the space domain
filteredImage = np.real(np.fft.ifft2(filteredSpectrum))

print(RMSE(reference, normalizeRange(filteredImage, 255, np.uint8)))