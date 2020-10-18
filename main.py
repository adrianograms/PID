import numpy as np
from PIL import Image

im = Image.open("mul.jpeg").convert("L")



kernel = np.zeros((3, 3), dtype=np.uint8)

image = np.asarray(im)

x = int(kernel.shape[0] / 2)
y = int(kernel.shape[1] / 2)

pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2), dtype=np.uint8)

pad_image[:] = 255

pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image



#convert back
im = Image.fromarray(np.uint8(pad_image))
im.show()