import numpy as np
from PIL import Image

im = Image.open("mul.jpeg").convert("L")


#8-neighbours
kernel = [i  for i in range(0,9)]

#4-neighbours
#kernel = [1,4,5,6,8]

#kernel = [0,4,7]

image = np.array(im)


x = 1
y = 1

pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2), dtype=np.uint8)

pad_image[:] = 1

pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image

for i in range(x,pad_image.shape[0]-x):
    for j in range(y,pad_image.shape[1]-y):
        aux = pad_image[i-x:i+x+1,j-y:j+y+1]
        image[i-x,j-y] = np.amax(aux.flatten()[kernel])



#convert back
im = Image.fromarray(np.uint8(image))
im.show()