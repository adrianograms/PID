import numpy as np
from PIL import Image

name_image = "Teste01"

im = Image.open("Folhas/" + name_image + ".png")

bg = 240

neighbours = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]]

border = []

image_copy = np.array(im)
image = np.array(im.convert("L"))

width = image.shape[0]
height = image.shape[1]

count = 0

#image = np.where(image < 240, image, 255)
#image = np.where(image > 240, image, 0)

for x in range(0,height):
  for y in range(0,width):
      if(image[x,y] < bg):
            origin = pq = (x,y)
            c = 0
            border.append((x,y))
            for _ in range(0, 8):
                i = pq[0] + neighbours[c][0]
                j = pq[1] + neighbours[c][1]
                if(image[i,j] < bg):
                    c = (c + 5)%8
                    border.append((i,j))
                    #image[i,j] = 155
                    pq = (i,j)
                    break
                c = (c + 1)%8
            while(pq != origin):
                for _ in range(0, 8):
                    i = pq[0] + neighbours[c][0]
                    j = pq[1] + neighbours[c][1]
                    if(image[i,j] < bg):
                        c = (c + 5)%8
                        border.append((i,j))
                        #image[i,j] = 155
                        pq = (i,j)
                        break
                    c = (c + 1)%8
            a = np.array(border)
            print(a)
            miny = np.min(a[:,0]) - 1
            maxy = np.max(a[:,0]) + 1
            minx = np.min(a[:,1]) - 1
            maxx = np.max(a[:,1]) + 1
            #print(miny, minx, maxy, maxx)
            image_color = image_copy[miny : maxy,  minx : maxx]
            Image.fromarray(np.uint8(image_color)).save("Imagens/" + name_image + "_" + str(count) + ".png")
            count = count + 1
            image[miny : maxy,  minx : maxx] = 255
            border = []
            #print(border)
            #Image.fromarray(np.uint8(image)).show()
            #exit()

Image.fromarray(np.uint8(image)).show()
#im = Image.fromarray(np.uint8(image))
