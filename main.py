import numpy as np
from PIL import Image
#joguei as funções para o arquivo morph.py
import morph as mp

im = Image.open("mul.jpeg").convert("L")

#Passa imagem e quantidade de interações
image = mp.erode(im,1)

#convert back
im = Image.fromarray(np.uint8(image))
im.show()