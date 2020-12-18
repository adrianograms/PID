from extract import foo
import numpy as np
import sys


def main():
    with open(sys.argv[1]) as f:
        for line in f:
            res = foo(line[:-1])
            np.savetxt('csv/' + line[:-1].split('/')[1][:-4] + '.csv',
                       res,
                       header='folha, media, variancia',
                       delimiter=',',
                       fmt='%1.5f')


if __name__ == '__main__':
    main()
