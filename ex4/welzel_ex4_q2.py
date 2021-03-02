import welzel_shared as sh
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import pyplot as plt

img_raw=sh.read_img("./imgs_ex4/image1_2021.fits")
img=np.array([row-np.mean(row) for row in img_raw])
print(img_raw)
print(img_raw-img)

fig, axs = plt.subplots(1, 2, constrained_layout=True)
fig.suptitle('Ex4, Q2 plots', fontsize=16)
plt.imshow(img_raw)
plt.imshow(img)
plt.show()




