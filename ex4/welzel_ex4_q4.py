import welzel_shared as sh
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
gau_sigma = 3
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, constrained_layout=False)
fig.suptitle('Ex4, Q4 a) plots. \n I also wanted to know what images 2 and 3 look like.', fontsize=16)
im1 = ax1.imshow(np.sum(img_raw[0], axis=0))
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Raw image data a).', fontsize=8)

im2 = ax2.imshow(gaussian_filter(np.sum(img_raw[0], axis=0), sigma=gau_sigma))
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="10%", pad=0.05)
cbar2 = plt.colorbar(im2, cax2)
ax2.set_title('Raw image data a) with gaussian filter.', fontsize=8)

im3 = ax3.imshow(np.sum(img_raw[1], axis=0))
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="10%", pad=0.05)
cbar3 = plt.colorbar(im3, cax3)
ax3.set_title('Raw image data b).', fontsize=8)

im4 = ax4.imshow(gaussian_filter(np.sum(img_raw[1], axis=0), sigma=gau_sigma))
divider4 = make_axes_locatable(ax4)
cax4 = divider4.append_axes("right", size="10%", pad=0.05)
cbar4 = plt.colorbar(im4, cax4)
ax4.set_title('Raw image data b) with gaussian filter.', fontsize=8)

im5 = ax5.imshow(np.sum(img_raw[2], axis=0))
divider5 = make_axes_locatable(ax5)
cax5 = divider5.append_axes("right", size="10%", pad=0.05)
cbar5 = plt.colorbar(im5, cax5)
ax5.set_title('Raw image data c).', fontsize=8)

im6 = ax6.imshow(gaussian_filter(np.sum(img_raw[2], axis=0), sigma=gau_sigma))
divider6 = make_axes_locatable(ax6)
cax6 = divider6.append_axes("right", size="10%", pad=0.05)
cbar6 = plt.colorbar(im6, cax6)
ax6.set_title('Raw image data c) with gaussian filter.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4a_plot.png", dpi=500)
plt.show()

fig, (ax1) = plt.subplots(1, 1, constrained_layout=False)
fig.suptitle('Ex4, Q4 a) plot.', fontsize=16)
im1 = ax1.imshow(sh.histogram_equalization(np.sum(img_raw[0], axis=0)))
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Raw image a, histogram equalized.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4a_2_plot.png", dpi=500)
plt.show()

print("a) the two dominant structures we see are: Hot and rouge pixels and (if we histogram equalize the images) we can also see the thermal straylight.")

sh.save_img_to_fits(np.sum(img_raw[0], axis=0),"./ex4","welzel_ex4_q4a_plot.fits")

# part B
# Ok first im finding the hot pixels and interpolating over them
# find hot pixel spots, just choose 1000 as cutoff, most other pixels are below 200
img_raw_hp_cleaned = np.where(img_raw > 1000, np.nan, img_raw)
img_raw_hp_cleaned = np.array([sh.interp_nan(img) for img in
                               img_raw_hp_cleaned.reshape(
                                   (-1, img_raw.shape[-2], img_raw.shape[-1]))])  # flex, but takes a bit of course
# better way to do this might be to just take the mean of the elements surrounding the nans
# TODO: implement multiprocessing for this so the TAs have to run it on linux

img_raw_hp_cleaned = img_raw_hp_cleaned.reshape(img_raw.shape)

# lets get the thermal stray light that you can see very clearly in the image now
# ill be using img_raw_hp_cleaned as the raw data now to get better performance
img_th_straylight = np.mean(img_raw_hp_cleaned.reshape((-1, img_raw.shape[-2], img_raw.shape[-1])), axis=0)

fig, (ax1) = plt.subplots(1, 1, constrained_layout=False)
fig.suptitle('Ex4, Q4 b) plot.', fontsize=16)
im1 = ax1.imshow(img_th_straylight)
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Sky only image.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4b_plot.png", dpi=500)
plt.show()

sh.save_img_to_fits(img_th_straylight,"./ex4","welzel_ex4_q4b_plot.fits")

# wow that looks real and smooth

# part C
img_flat_field_raw = np.array(sh.read_img(f"./ex4/imgs_ex4/flat3_2021.fits"))
img_norm_flat_field = img_flat_field_raw / np.mean(img_flat_field_raw)

img_flat_field_re_scaled = np.array([img_norm_flat_field for img in img_raw_hp_cleaned
                                    .reshape((-1, img_raw.shape[-2], img_raw.shape[-1]))]) \
    .reshape(img_raw.shape)

fig, (ax1) = plt.subplots(1, 1, constrained_layout=False)
fig.suptitle('Ex4, Q4 c) plot.', fontsize=16)
im1 = ax1.imshow(img_norm_flat_field)
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Flat field normalized by mean.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4c_plot.png", dpi=500)
plt.show()

sh.save_img_to_fits(img_norm_flat_field,"./ex4","welzel_ex4_q4c_plot.fits")

# part D
# ok, lets do it
# we already have the imgs with the hotpixels removed, let remove the thermal straylight from them
img = img_raw_hp_cleaned-img_th_straylight

# this is here so we have an image before the subtraction of the flat field
img_comp = np.sum(img, axis=1)[0, :, 0:-60] + np.sum(img, axis=1)[1, :, 30:-30] + np.sum(img, axis=1)[2, :, 60:]

# now lets remove the flat field from them
img=img/img_flat_field_re_scaled*np.mean(img_flat_field_re_scaled)

# summing up the images with the same telescope orientation
img_summed = np.sum(img, axis=1)

# super positioning of the images
img_region = img_summed[0, :, 0:-60] + img_summed[1, :, 30:-30] + img_summed[2, :, 60:]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=False)
fig.suptitle('Ex4, Q4 d) plots.', fontsize=16)
im1 = ax1.imshow(img_region)
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="10%", pad=0.05)
cbar1 = plt.colorbar(im1, cax1)
ax1.set_title('Final image.', fontsize=8)

im2 = ax2.imshow(gaussian_filter(img_region, sigma=gau_sigma))
ax2.scatter(x=34, y=75, c='black', marker="+", s=1)
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="10%", pad=0.05)
cbar2 = plt.colorbar(im2, cax2)
ax2.set_title('Final image with gaussian filter.', fontsize=8)

im3 = ax3.imshow(img_comp)
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="10%", pad=0.05)
cbar3 = plt.colorbar(im3, cax3)
ax3.set_title('Final image without flat field removed.', fontsize=8)

im4 = ax4.imshow(gaussian_filter(img_comp, sigma=gau_sigma))
ax4.scatter(x=34, y=75, c='black', marker="+", s=1)
divider4 = make_axes_locatable(ax4)
cax4 = divider4.append_axes("right", size="10%", pad=0.05)
cbar4 = plt.colorbar(im4, cax4)
ax4.set_title('Final image without flat field removed with gaussian filter.', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./ex4/welzel_ex4_q4d_plot.png", dpi=500)
plt.show()

print("d) the approximate position of the brown dwarf is x=34px , y=75px (my processed image) or x=64px , y=75px (raw image b).")

sh.save_img_to_fits(img_region,"./ex4","welzel_ex4_q4d_plot.fits")
sh.save_img_to_fits(gaussian_filter(img_region, sigma=gau_sigma),"./ex4","welzel_ex4_q4d_gau_filt_plot.fits")

# fig, (ax1, ax3) = plt.subplots(2, 1, constrained_layout=False)
# fig.suptitle('Plot so you see whats going on.', fontsize=16)
# im1 = ax1.imshow(img_summed[0])
# divider1 = make_axes_locatable(ax1)
# cax1 = divider1.append_axes("right", size="10%", pad=0.05)
# cbar1 = plt.colorbar(im1, cax1)
# ax1.set_title('Final image (with flat field subtracted), looks just like the inverse of the flat field!', fontsize=8)
#
# im3 = ax3.imshow(img_norm_flat_field)
# divider3 = make_axes_locatable(ax3)
# cax3 = divider3.append_axes("right", size="10%", pad=0.05)
# cbar3 = plt.colorbar(im3, cax3)
# ax3.set_title('Flat field normalized by mean (compare with above).', fontsize=8)
#
# plt.tight_layout()
# plt.subplots_adjust(top=0.85)
# plt.savefig("./ex4/welzel_ex4_q4d_addendum_plot.png", dpi=500)
# plt.show()
#
# fig, (ax1) = plt.subplots(1, 1, constrained_layout=False)
# fig.suptitle('Ex4, Q4 d) straight superposition.', fontsize=16)
# im1 = ax1.imshow(np.sum(img,axis=(0,1)))
# divider1 = make_axes_locatable(ax1)
# cax1 = divider1.append_axes("right", size="10%", pad=0.05)
# cbar1 = plt.colorbar(im1, cax1)
# ax1.set_title('Final images superposition (30px offset for the star/ no offset of the raw images).', fontsize=8)
#
# plt.tight_layout()
# plt.subplots_adjust(top=0.85)
# plt.savefig("./ex4/welzel_ex4_q4d_addendum2_plot.png", dpi=500)
# plt.show()