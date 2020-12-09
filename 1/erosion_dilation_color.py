from PIL import Image
import numpy as np
import time

def erosion(kernel, name_file):
    im = Image.open(name_file)
    image = im.convert('L')

    x = int(kernel.shape[0] / 2)
    y = int(kernel.shape[1] / 2)

    pad_image = np.zeros((image.height + x * 2, image.width + y * 2), dtype=np.uint8)
    pad_image[:] = 255

    new_image = np.zeros((image.height, image.width, 3))

    pad_image[x:x + image.height, y:y + image.width] = image

    for x_image in range(image.height):
        for y_image in range(image.width):
            valor = (pad_image[x_image + x][y_image + y],(x_image + x, y_image + y))
            for x_kernal in range(kernel.shape[0]):
                for y_kernal in range(kernel.shape[1]):
                    if kernel[x_kernal][y_kernal] == 0:
                        continue
                    if pad_image[x_image + x_kernal][y_image + y_kernal] < valor[0]:
                        valor = (pad_image[x_image + x_kernal][y_image + y_kernal], (x_image + x_kernal, y_image + y_kernal))
            new_image[x_image][y_image] = im.getpixel((valor[1][1] - x,valor[1][0] - y))
    fim = Image.fromarray(np.uint8(new_image)).convert('RGB')
    fim.show()
    fim.save("erosion_" + name_file)

def dilation(kernel, name_file):
    im = Image.open(name_file)
    image = im.convert('L')

    x = int(kernel.shape[0] / 2)
    y = int(kernel.shape[1] / 2)

    pad_image = np.zeros((image.height + x * 2, image.width + y * 2), dtype=np.uint8)
    pad_image[:] = 0

    new_image = np.zeros((image.height, image.width, 3))

    pad_image[x:x + image.height, y:y + image.width] = image

    for x_image in range(image.height):
        for y_image in range(image.width):
            valor = (pad_image[x_image + x][y_image + y],(x_image + x, y_image + y))
            for x_kernal in range(kernel.shape[0]):
                for y_kernal in range(kernel.shape[1]):
                    if kernel[x_kernal][y_kernal] == 0:
                        continue
                    if pad_image[x_image + x_kernal][y_image + y_kernal] > valor[0]:
                        valor = (pad_image[x_image + x_kernal][y_image + y_kernal], (x_image + x_kernal, y_image + y_kernal))
            new_image[x_image][y_image] = im.getpixel((valor[1][1] - x,valor[1][0] - y))
    fim = Image.fromarray(np.uint8(new_image)).convert('RGB')
    fim.show()
    fim.save("dilation_" + name_file)


name_file = "mul.jpeg"

kernel = (3,3)
kernel = np.zeros(kernel, dtype=np.uint8)
kernel[:] = 1

# erosion(kernel, name_file)
dilation(kernel, name_file)

#--------------------------------------------------------------------------------------------------------------------------
# Fim da aplicação
#--------------------------------------------------------------------------------------------------------------------------

# Nada de importante aqui embaixo, só deixei por garantia

#image.show()

# kernel = np.zeros(kernel, dtype=np.uint8)
# kernal

# x = int(kernel.shape[0] / 2)
# y = int(kernel.shape[1] / 2)

# pad_image = np.zeros((image.height + x * 2, image.width + y * 2), dtype=np.uint8)
# pad_image[:] = 255
# new_image = np.zeros((image.height, image.width, 3))


# pad_image[x:x + image.height, y:y + image.width] = image
# print(pad_image.shape[0], pad_image.shape[1])
# print(image.height)

# #im = Image.fromarray(np.uint8(pad_image))
# #im.show()

# for x_image in range(image.height):
#     for y_image in range(image.width):
#         valor = (pad_image[x_image + x][y_image + y],(x_image + x, y_image + y))
#         for x_kernal in range(kernel.shape[0]):
#             for y_kernal in range(kernel.shape[1]):
#                 if kernel[x_kernal][y_kernal] == 0:
#                     continue
#                 if pad_image[x_image + x_kernal][y_image + y_kernal] < valor[0]:
#                     valor = (pad_image[x_image + x_kernal][y_image + y_kernal], (x_image + x_kernal, y_image + y_kernal))
#         new_image[x_image][y_image] = im.getpixel((valor[1][1] - x,valor[1][0] - y))
# #fim = Image.fromarray(new_image) 
# fim = Image.fromarray(np.uint8(new_image)).convert('RGB')
# fim.show()



#print(im.getpixel((1000,10)))
#print(a)
