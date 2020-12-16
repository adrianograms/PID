from PIL import Image
from extract import foo
import sys

def main():

    with open(sys.argv[1]) as files:
        for line in files:
            foo(line[:-1])


if __name__ == '__main__':
    main()
