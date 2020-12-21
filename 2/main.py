from extract import foo
import numpy as np
import sys


fmt = '%d', '%d', '%1.5f', '%1.5f'


def main():
    with open(sys.argv[1]) as f:
        for line in f:
            if(len(line) < 3):
                continue
            print("Processamento da imagem", line.split("\n")[0])
            res = foo(line.split("\n")[0])
            aux = line[:-1].split("/")
            np.savetxt('csv/' + aux[len(aux)-1].split(".")[0] + '.csv',
                       res,
                       header='folha, perimetro, media, variancia',
                       delimiter=', ',
                       fmt=fmt)
            print("Imagem processada!\n")


if __name__ == '__main__':
    main()
