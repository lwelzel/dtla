import welzel_shared as sh
import pprint
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import gaussian_filter
import os

img_raw = sh.read_img("./ex4/imgs_ex4/image2_2021.fits")

unexposed_columns = img_raw[:, 0:4]
noise = np.resize(np.mean(unexposed_columns, axis=1), img_raw.shape).T

# only care about exposed pixels
img = (img_raw - noise)[:, 5:]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=False)
fig.suptitle('Ex4, Q3 plots. \n All processed images only show the exposed pixels.', fontsize=16)
im1 = ax1.imshow(img_raw)
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Raw image data.', fontsize=8)

im2 = ax2.imshow(img)
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="10%", pad=0.05)
cbar2 = plt.colorbar(im2, cax2)
ax2.set_title('Processed image data.', fontsize=8)

# just to flex
im3 = ax3.imshow(gaussian_filter(sh.histogram_equalization(img), sigma=12))
ax3.scatter(x=195, y=375, c='navy', marker='+')
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="10%", pad=0.05)
cbar3 = plt.colorbar(im3, cax3)
ax3.set_title('Histogram equalized & Gaussian filter.', fontsize=8)

im4 = ax4.imshow(gaussian_filter(img, sigma=12))
divider4 = make_axes_locatable(ax4)
cax4 = divider4.append_axes("right", size="10%", pad=0.05)
cbar4 = plt.colorbar(im4, cax4)
ax4.set_title('Gaussian filter.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q3_plot.png")
plt.show()

# Answers:
