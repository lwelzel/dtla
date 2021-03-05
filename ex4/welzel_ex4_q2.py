import welzel_shared as sh
import pprint
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import gaussian_filter

img_raw = sh.read_img("./ex4/imgs_ex4/image1_2021.fits")
channels = np.array([np.arange(start, 128, 4) for start in np.arange(4)])

means = np.array([np.mean(img_raw[:, channels[i]]) for i in np.arange(4)])
offset_levels = means
means = np.tile(means, int(128 / 4))  # TODO kinda shitty way to do it but its like 23:30 and I want to sleep

img = img_raw - means

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=False)
fig.suptitle('Ex4, Q2 plots. \n Lower two are a bonus!', fontsize=16)
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
im3 = ax3.imshow(gaussian_filter(sh.histogram_equalization(img), sigma=5))
ax3.scatter(x=35, y=85, c='navy', marker='+')
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="10%", pad=0.05)
cbar3 = plt.colorbar(im3, cax3)
ax3.set_title('Histogram equalized & Gaussian filter.', fontsize=8)

im4 = ax4.contourf(np.exp(img), levels=10, cmap='gist_heat')  # plotted is exp(data)
ax4.set_aspect('equal')
ax4.invert_yaxis()
divider4 = make_axes_locatable(ax4)
cax4 = divider4.append_axes("right", size="10%", pad=0.05)
cbar4 = plt.colorbar(im4, cax4)
ax4.set_title('Contoured because I like plots.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q2_plot.png")
plt.show()

# Answers:
print("Q2 a)")
channel_names = [f"Offset Channel {i}: " for i in range(1, 5)]
ans_a = dict(zip(channel_names, offset_levels))
pprint.pp(ans_a, width=-1)

print("\nQ2 b)")
ans_b = dict(zip(['x', 'y'], [35, 85]))
pprint.pp(ans_b, width=-1)
print("See Hist. Equ. & Gauss. Filt. plot. \nThe Hist. Equ. enhances global contrast &"
      " the guassian filter filters out what might be hot pixels/ less luminous objects.")

sh.save_img_to_fits(img,"./ex4","welzel_ex4_q2_plot.fits")

