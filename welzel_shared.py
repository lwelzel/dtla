import numpy as np


def read_img(loc):
    '''
    extract data arrays from .fits files
    :param loc: (str) filepaths to images
    :return: (np.array) array for .fits data. Shape=(len(loc),420,1020)
    '''
    from astropy.io import fits
    from astropy.utils.data import get_pkg_data_filename
    image_files = get_pkg_data_filename(loc)
    print(f"---====== Reading {loc} image. ======---")
    fits.info(image_files)
    print(f"---==========================================---\n")
    # TODO: this is pretty horrible but works well enough and I dont care about that part of the images
    # WARN: if the image_data is not all of exact equal dimensions then numpy operations dont work well of course
    # (list-of_tuples, etc)
    image_data = fits.getdata(image_files, ext=0)
    return image_data


def histogram_equalization(img, n_bins=256):
    '''
    based on https://en.wikipedia.org/wiki/Histogram_equalization
    :param img: (np.array) image to be used
    :param n_bins: (int) number of bins, typically 256
    :return: (np.array) histogram equalized image
    '''
    # TODO: found code using skimage.exposure.cumulative_distribution(), might be faster

    # determine hist and bins using np, get cdf and normalize cdf
    image_histogram, bins = np.histogram(img.flatten(), n_bins, density=True)
    cdf = image_histogram.cumsum()
    cdf = (n_bins - 1) * cdf / cdf[-1]

    # find new values from cdf
    img_hist_equ = np.interp(img.flatten(), bins[:-1], cdf)

    return img_hist_equ.reshape(img.shape)

def interp_nan(img, method='linear'):
    '''
    cleans up nan data in 2d arrays. Intended use is images.
    :param img: (2d array)
    :param method: ('nearest', linear’, ‘cubic’)
    :return: cleaned 2d array
    '''
    from scipy.interpolate import griddata
    grid_x, grid_y = np.mgrid[0:img.shape[0], 0:img.shape[1]]

    img_masked=np.ma.array(img, mask=np.isnan(img)).compressed().flatten()

    grid_masked = np.stack((np.ma.array(grid_x, mask=np.isnan(img)).compressed().flatten(),
                             np.ma.array(grid_y, mask=np.isnan(img)).compressed().flatten())).T

    img=griddata(points= grid_masked, values=img_masked, xi=(grid_x, grid_y), method=method)
    return img

# # set dir path for anything using welzel_shared
# os.chdir("/home/lwelzel/Documents/Git/dtla/")
