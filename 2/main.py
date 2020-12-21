from extract import foo
import numpy as np
import sys


fmt = '%d', '%d', '%1.5f', '%1.5f'


def main():
    with open(sys.argv[1]) as f:
        for line in f:
            print("Processamento da imagem", line)
            res = foo(line[:-1])
            np.savetxt('csv/' + line[:-1].split('/')[1][:-4] + '.csv',
                       res,
                       header='folha, perimetro, media, variancia',
                       delimiter=', ',
                       fmt=fmt)
            print("Imagem processada!")


if __name__ == '__main__':
    main()
