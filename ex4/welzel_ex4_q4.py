import welzel_shared as sh
import pprint
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import gaussian_filter

# praise numpy and equal image sizes
img_raw = np.array([sh.read_img(f"./ex4/imgs_ex4/image3{n}_2021.fits") for n in ["a", "b", "c"]])

# part a)
gau_sigma=3
fig, ((ax1, ax2),(ax3, ax4),(ax5, ax6)) = plt.subplots(3, 2, constrained_layout=False)
fig.suptitle('Ex4, Q4 a) plots. \n I also wanted to know what images2 and 3 look like.', fontsize=16)
im1 = ax1.imshow(np.sum(img_raw[0],axis=0))
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Raw image data a).', fontsize=8)

im2 = ax2.imshow(gaussian_filter(np.sum(img_raw[0],axis=0), sigma=gau_sigma))
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="10%", pad=0.05)
cbar2 = plt.colorbar(im2, cax2)
ax2.set_title('Raw image data a) with gaussian filter.', fontsize=8)

im3 = ax3.imshow(np.sum(img_raw[1],axis=0))
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="10%", pad=0.05)
cbar3 = plt.colorbar(im3, cax3)
ax3.set_title('Raw image data b).', fontsize=8)

im4 = ax4.imshow(gaussian_filter(np.sum(img_raw[1],axis=0), sigma=gau_sigma))
divider4 = make_axes_locatable(ax4)
cax4 = divider4.append_axes("right", size="10%", pad=0.05)
cbar4 = plt.colorbar(im4, cax4)
ax4.set_title('Raw image data b) with gaussian filter.', fontsize=8)

im5 = ax5.imshow(np.sum(img_raw[2],axis=0))
divider5 = make_axes_locatable(ax5)
cax5 = divider5.append_axes("right", size="10%", pad=0.05)
cbar5 = plt.colorbar(im5, cax5)
ax5.set_title('Raw image data c).', fontsize=8)

im6 = ax6.imshow(gaussian_filter(np.sum(img_raw[2],axis=0), sigma=gau_sigma))
divider6 = make_axes_locatable(ax6)
cax6 = divider6.append_axes("right", size="10%", pad=0.05)
cbar6 = plt.colorbar(im6, cax6)
ax6.set_title('Raw image data c) with gaussian filter.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4a_plot.png", dpi=500)
plt.show()

print("a) the two dominant structures we see are: Hot and rouge pixels")
print("a) as you can see gaussian filtering is very op.\n There is a hot spot on the right moving is positive y direction consistantly over the images.")

# part B

sky_only=np.where((img_raw[0]==img_raw[1]), img_raw[0], np.zeros_like(img_raw[0])) #and (img_raw[0]=img_raw[2])
print(sky_only)
print(sky_only.shape)
plt.imshow(sky_only)
plt.show()