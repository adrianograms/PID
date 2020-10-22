from PIL import Image
import morph as mp
import numpy as np
import getopt
import sys
import time 


def get_structuring_element(morph, size):
    if morph == 'cross':
        k = np.zeros((size, size), dtype=np.uint8)
        k[:, int(size / 2)] = 1
        k[int(size / 2), :] = 1
        return k

    return np.ones((size, size), dtype=np.uint8)


def read_kernel(size):
    k = np.empty((size, size), dtype=np.uint8)

    # achar uma maneira melhor de fazer isso?
    for i in range(size):
        for j in range(size):
            k[i][j] = 0 if int(input()) == 0 else 1

    return k


def main():
    in_file_name = None
    out_file_name = None
    kernel = None
    kernel_size = None
    mopt = None                  # 0 = erode, 1 = dilate

    iterations = 1

    custom_kernel = False

    mopts = [mp.erode, mp.dilate]

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:m:s:r:edc')
        # -i nome do arquivo de entrada
        # -o nome do arquivo de saida
        # -m tipo do kernel
        # -s tamanho de kernel (sempre quadrado)
        # -r numero de iteracoes
        # -e erode
        # -d dilate
        # -c ler kernel do user
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-i':
            in_file_name = arg
        elif opt == '-o':
            out_file_name = arg
        elif opt == '-m':
            kernel = arg
        elif opt == '-s':
            kernel_size = int(arg)
        elif opt == '-c':
            custom_kernel = True
        elif opt == '-r':
            iterations = int(arg)
        elif opt == '-e':
            mopt = 0
        elif opt == '-d':
            mopt = 1

    if None in (in_file_name, out_file_name, kernel_size, mopt) and not custom_kernel:
        print('Error: Missing paramether')
        sys.exit(1)

    if kernel_size == 1 or kernel_size % 2 == 0:
        print('Error: Kernel size must be odd and bigger than 1')
        sys.exit(1)

    if custom_kernel:
        kernel = read_kernel(kernel_size)
    elif kernel in ('cross', 'rectangle'):
        kernel = get_structuring_element(kernel, kernel_size)
    else:
        print('Error: Invalid kernel paramether')

    im = []
    try:
        im = Image.open(in_file_name).convert('L')

    except:
        print(f'Error: Fail to open image {in_file_name}')
        sys.exit(1)

    # Passa imagem e quantidade de interações
    start = time.time()
    image = mopts[mopt](np.array(im, dtype=np.uint8), kernel, iterations)
    print(time.time() - start)

    # convert back
    im = Image.fromarray(np.uint8(image))
    im.save(out_file_name)
    im.show()


if __name__ == '__main__':
    main()
