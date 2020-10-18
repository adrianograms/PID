import numpy as np
from PIL import Image

def erode(im, iterations = 1):
    #Uma outra ideia para pegar o vetor de indices
    k = np.ones((3,3),dtype=np.uint8).flatten()
    kernel = [i for i in range(len(k)) if k[i]]

    #convert to np array
    image = np.array(im)


    x = 1
    y = 1
    for _ in range(iterations):
      pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2), dtype=np.uint8)

      pad_image[:] = 255

      pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image

    
      for i in range(x,pad_image.shape[0]-x):
        for j in range(y,pad_image.shape[1]-y):
          aux = pad_image[i-x:i+x+1,j-y:j+y+1]
          image[i-x,j-y] = np.amin(aux.flatten()[kernel])

    return image


def dilate(im, iterations = 1):
    #Uma outra ideia para pegar o vetor de indices
    k = np.ones((3,3),dtype=np.uint8).flatten()
    kernel = [i for i in range(0,len(k)) if k[i]]

    #convert to np array
    image = np.array(im)


    x = 1
    y = 1
    for _ in range(iterations):
      pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2), dtype=np.uint8)

      pad_image[:] = 0

      pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image

      for i in range(x,pad_image.shape[0]-x):
        for j in range(y,pad_image.shape[1]-y):
          aux = pad_image[i-x:i+x+1,j-y:j+y+1]
          image[i-x,j-y] = np.amax(aux.flatten()[kernel])

    return image

