#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Image

q = raw_input('Enter Team: ')
image = Image.open('images/' + q + '.jpg')

arr = np.asarray(image)
plt.imshow(arr)
plt.show()
