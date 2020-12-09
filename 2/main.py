import numpy as np
from PIL import Image

im = Image.open("Folhas/Teste01.png")

bg = np.array([255,255,255])


image = np.array(im)
width = image.shape[0]
height = image.shape[1]

for i in range(0,height):
  for j in range(0,width):
      if(not (image[i,j] == bg).all()):
          foo(image[i,j], i, j)

def foo(ponto, p, q):
    i = p
    j = q

    q = q-1





im = Image.fromarray(np.uint8(image))
