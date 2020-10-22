import numpy as np


def kernel_to_index(kernel):
    fkernel = kernel.flatten()

    return [i for i in range(len(fkernel)) if fkernel[i] != 0]


def erode(image, kernel, iterations=1):
    ikernel = kernel_to_index(kernel)

    x = int(kernel.shape[0] / 2)
    y = int(kernel.shape[1] / 2)

    pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2),
                         dtype=np.uint8)

    pad_image[:] = 255

    for _ in range(iterations):
        pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image

        for i in range(x, pad_image.shape[0] - x):
            for j in range(y, pad_image.shape[1] - y):
                image[i - x, j - y] = np.amin(pad_image[i - x:i + x + 1,
                                                        j - y:j + y + 1]
                                              .flatten()[ikernel])

    return image


def dilate(image, kernel, iterations=1):
    ikernel = kernel_to_index(kernel)

    x = int(kernel.shape[0] / 2)
    y = int(kernel.shape[1] / 2)

    pad_image = np.zeros((image.shape[0] + x * 2, image.shape[1] + y * 2),
                         dtype=np.uint8)

    pad_image[:] = 0

    for _ in range(iterations):
        pad_image[x:x + image.shape[0], y:y + image.shape[1]] = image

        for i in range(x, pad_image.shape[0] - x):
            for j in range(y, pad_image.shape[1] - y):
                image[i - x, j - y] = np.amax(pad_image[i - x:i + x + 1,
                                                        j - y:j + y + 1]
                                              .flatten()[ikernel])

    return image
