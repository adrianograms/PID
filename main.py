#!/usr/bin/env python

from PIL import Image
import morph as mp
import numpy as np
import getopt
import sys


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


def usage():
    print("Os parâmetros para o programa são os seguintes:\n\
    -i = Nome do arquivo de entrada. Por exemplo: -i test.png\n\
    -o = Nome do arquivo de saída. Por exemplo: -o test_out.jpg\n\
    -m = O tipo do kernel/elemento estruturante, este pode ser cross ou\
rectangle. Por exemplo: -m cross.\n\
    -s = O tamanho kernel/elemento estruturante, este valor deve ser maior do\
que 1 e ímpar. Por exemplo: -s 3.\n\
    -r = O número de iterações, valor padrão = 1. Por exemplo -r 10.\n\
    -e = Escolhe a operação morfológica de erosão.\n\
    -d = Escolha a operação morfológica de dilatação.\n\
    -c = Le um kernel/elemento estruturante de tamanho dado por -s do usuário.\
    \n\
    ")


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
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:m:s:r:edch')
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
            try:
                kernel_size = int(arg)
            except:
                print('Error: Kernel size must be a number')
                usage()
                sys.exit(1)
        elif opt == '-c':
            custom_kernel = True
        elif opt == '-r':
            try:
                iterations = int(arg)
            except:
                print('Error: Number of iterations must be a number')
                usage()
                sys.exit(1)
            if iterations <= 0:
                print('Error: Number of iterations must be possitive and \
bigger than zero')
                usage()
                sys.exit(1)
        elif opt == '-e':
            mopt = 0
        elif opt == '-d':
            mopt = 1
        elif opt == '-h':
            usage()
            sys.exit(1)

    if None in (in_file_name, out_file_name,
                kernel_size, mopt) and not custom_kernel:
        print('Error: Missing paramether')
        usage()
        sys.exit(1)

    if kernel_size == 1 or kernel_size % 2 == 0:
        print('Error: Kernel size must be odd and bigger than 1')
        usage()
        sys.exit(1)

    if custom_kernel:
        kernel = read_kernel(kernel_size)
    elif kernel in ('cross', 'rectangle'):
        kernel = get_structuring_element(kernel, kernel_size)
    else:
        print('Error: Invalid kernel paramether')
        usage()
        sys.exit(1)

    im = []
    try:
        im = Image.open(in_file_name).convert('L')

    except:
        print(f'Error: Fail to open image {in_file_name}')
        sys.exit(1)

    # Passa imagem e quantidade de interações
    image = mopts[mopt](np.array(im, dtype=np.uint8), kernel, iterations)

    # convert back
    im = Image.fromarray(np.uint8(image))
    im.save(out_file_name)
    # im.show()


if __name__ == '__main__':
    main()
