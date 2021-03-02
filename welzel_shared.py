import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser'
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import io
from scipy import stats

def read_img(loc):
    '''
    extract data arrays from .fits files
    :param loc: (str) filepaths to images
    :return: (np.array) array for .fits data. Shape=(len(loc),420,1020)
    '''
    image_files=get_pkg_data_filename(loc)
    print(f"---====== Reading {loc} image. ======---")
    fits.info(image_files)
    print(f"---==========================================---")
    # TODO: this is pretty horrible but works well enough and I dont care about that part of the images
    # WARN: if the image_data is not all of exact equal dimensions then numpy operations dont work well of course
    # (list-of_tuples, etc)
    image_data = fits.getdata(image_files, ext=0)
    return image_data