# ALS - Astro Live Stacker
# Copyright (C) 2019  Sébastien Durand (Dragonlost) - Gilles Le Maréchal (Gehelem)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import astroalign as al
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm

plt.ion()

nb_im = np.arange(19) + 2
nb_im_str = []
for i in nb_im:
    nb_im_str.append("%05d" % i)

image = fits.open("light_00001.fit")
rgb_ref = image[0].data
image.close()

for i in tqdm(nb_im_str):
    image = fits.open("light_"+str(i)+".fit")
    rgb_new = image[0].data
    image.close()

    p, (pos_img, pos_img_rot) = al.find_transform(rgb_new[1], rgb_ref[1])
    rgb_align = []
    for j in tqdm(range(3)):
        rgb_align.append(al.apply_transform(p, rgb_new[j], rgb_ref[j])+rgb_ref[j])
        rgb_align[j] = np.where(rgb_align[j] < 65535, rgb_align[j], 65535)
    rgb_ref = rgb_align
new_rvb = np.rollaxis((np.array(rgb_ref) / 65535.) ** (1 / 3.), 0, 3)
plt.imshow(new_rvb)

