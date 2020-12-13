import numpy as np
from PIL import Image


def floodfill(image, y,x, bg, limit):

  #limit = [minx, maxx, miny, maxy]
  new_image = np.zeros((limit[1]-limit[0],limit[3]-limit[2],3), dtype=int)
  new_image[:] = [255, 255, 255]
  q = [(y,x)]
  bg_color = np.array([255,255,255])
  new_image[y - limit[2], x - limit[0]] = image[y,x]
  image[y,x] = bg_color

  while(len(q)):
    pos = q[0]
    q.pop(0)

    if(image[pos[0],pos[1]+1].mean() < bg):
      q.append((pos[0],pos[1]+1))
      new_image[pos[0] - limit[2], pos[1]+1 - limit[0]] = image[pos[0],pos[1]+1]
      image[pos[0],pos[1]+1] = bg_color

    if(image[pos[0],pos[1]-1].mean() < bg):
      q.append((pos[0],pos[1]-1))
      new_image[pos[0] - limit[2], pos[1]-1 - limit[0]] = image[pos[0],pos[1]-1]
      image[pos[0],pos[1]-1] = bg_color

    if(image[pos[0]-1,pos[1]].mean() < bg):
      q.append((pos[0]-1,pos[1]))
      new_image[pos[0]-1 - limit[2], pos[1] - limit[0]] = image[pos[0]-1,pos[1]]
      image[pos[0]-1,pos[1]] = bg_color

    if(image[pos[0]+1,pos[1]].mean() < bg):
      q.append((pos[0]+1,pos[1]))
      new_image[pos[0]+1 - limit[2], pos[1] - limit[0]] =  image[pos[0]+1,pos[1]]
      image[pos[0]+1,pos[1]] = bg_color
  return new_image

def foo(file):
    name_image = file[7:-4]

    im = Image.open(file)

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
                            pq = (i,j)
                            break
                        c = (c + 1)%8
                a = np.array(border)
                miny = np.min(a[:,0]) - 1
                maxy = np.max(a[:,0]) + 50
                minx = np.min(a[:,1]) - 1
                maxx = np.max(a[:,1]) + 50
                limit = [minx, maxx, miny, maxy]
                if(len(border) > 20):
                    image_color = floodfill(image_copy, border[0][0],border[0][1], bg, limit)
                    Image.fromarray(np.uint8(image_color)).save("Imagens/" + name_image + "_" + str(count) + ".png")
                    count = count + 1

                if(count > 0):
                    Image.fromarray(np.uint8(image_copy)).show()
                    return
                border = []


    #im = Image.fromarray(np.uint8(image))
