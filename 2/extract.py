import numpy as np
#import cv2 as cv
from PIL import Image

def check_limit(shape, i, j):
    if(i >= 0 and j >=0 and i < shape[0] and j < shape[1]):
        return True
    return False


def floodfill(image, y,x, bg, limit, image_grayscale):

  #limit = [minx, maxx, miny, maxy]
  print(limit)
  print(y, x)
  new_image = np.zeros((limit[3]-limit[2],limit[1]-limit[0],3), dtype=int)
  new_image[:] = [255, 255, 255]
  q = [(y,x)]
  #bg = 220
  #bg_color = np.array([255,255,255])
  bg_color = [255,255,255]
  new_image[y - limit[2], x - limit[0]] = image[y,x]
  image[y,x] = bg_color
  image_grayscale[y,x] = 255

  while(len(q)):
    pos = q[0]
    q.pop(0)

    if(image_grayscale[pos[0],pos[1]+1] < bg and check_limit(image_grayscale.shape, pos[0], pos[1] + 1)):
      q.append((pos[0],pos[1]+1))
      new_image[pos[0] - limit[2], pos[1]+1 - limit[0]] = image[pos[0],pos[1]+1]
      #image[pos[0],pos[1]+1] = bg_color
      image_grayscale[pos[0],pos[1]+1] = 255

    if(image_grayscale[pos[0],pos[1]-1] < bg and check_limit(image_grayscale.shape, pos[0], pos[1] - 1)):
      q.append((pos[0],pos[1]-1))
      new_image[pos[0] - limit[2], pos[1]-1 - limit[0]] = image[pos[0],pos[1]-1]
      #image[pos[0],pos[1]-1] = bg_color
      image_grayscale[pos[0],pos[1]-1] = 255

    if(image_grayscale[pos[0]-1,pos[1]] < bg and check_limit(image_grayscale.shape, pos[0] - 1, pos[1])):
      q.append((pos[0]-1,pos[1]))
      new_image[pos[0]-1 - limit[2], pos[1] - limit[0]] = image[pos[0]-1,pos[1]]
      #image[pos[0]-1,pos[1]] = bg_color
      image_grayscale[pos[0]-1,pos[1]] = 255

    if(image_grayscale[pos[0]+1,pos[1]] < bg and check_limit(image_grayscale.shape, pos[0] + 1, pos[1])):
      q.append((pos[0]+1,pos[1]))
      new_image[pos[0]+1 - limit[2], pos[1] - limit[0]] =  image[pos[0]+1,pos[1]]
      #image[pos[0]+1,pos[1]] = bg_color
      image_grayscale[pos[0]+1,pos[1]] = 255

    if(image_grayscale[pos[0]+1,pos[1]+1] < bg and check_limit(image_grayscale.shape, pos[0] + 1, pos[1] + 1)):
      q.append((pos[0]+1,pos[1]+1))
      new_image[pos[0]+1 - limit[2], pos[1]+1 - limit[0]] = image[pos[0]+1,pos[1]+1]
      #image[pos[0]+1,pos[1]+1] = bg_color
      image_grayscale[pos[0]+1,pos[1]+1] = 255

    if(image_grayscale[pos[0]-1,pos[1]-1] < bg and check_limit(image_grayscale.shape, pos[0] - 1, pos[1] - 1)):
      q.append((pos[0]-1,pos[1]-1))
      new_image[pos[0]-1 - limit[2], pos[1]-1 - limit[0]] = image[pos[0]-1,pos[1]-1]
      #image[pos[0]-1,pos[1]-1] = bg_color
      image_grayscale[pos[0]-1,pos[1]-1] = 255

    if(image_grayscale[pos[0]-1,pos[1]+1] < bg and check_limit(image_grayscale.shape, pos[0] - 1, pos[1] + 1)):
      q.append((pos[0]-1,pos[1]+1))
      new_image[pos[0]-1 - limit[2], pos[1]+1 - limit[0]] = image[pos[0]-1,pos[1]+1]
      #image[pos[0]-1,pos[1]+1] = bg_color
      image_grayscale[pos[0]-1,pos[1]+1] = 255
      
    if(image_grayscale[pos[0]+1,pos[1]-1] < bg and check_limit(image_grayscale.shape, pos[0] + 1, pos[1] - 1)):
      q.append((pos[0]+1,pos[1]-1))
      new_image[pos[0]+1 - limit[2], pos[1]-1 - limit[0]] =  image[pos[0]+1,pos[1]-1]
      #image[pos[0]+1,pos[1]-1] = bg_color
      image_grayscale[pos[0]+1,pos[1]-1] = 255
  return new_image

def foo(file):
    name_image = file[7:-4]

    im = Image.open(file).convert("RGB")

    bg = 220
    neighbours = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]]

    border = []

    image_copy = np.array(im)
    
    image = np.array(im.convert("L"))

    height = image.shape[0]
    width = image.shape[1]

    #image = np.where(image < bg, image, 255)
    #image = np.where(image > bg, image, 0)

    #kernel = np.ones((5,5),np.uint8)
    #image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)

    count = 0

    for x in range(0,height):
      for y in range(0,width):
          if(image[x,y] < bg):
                origin = pq = (x,y)
                c = 0
                border.append((x,y))
                for _ in range(0, 8):
                    i = pq[0] + neighbours[c][0]
                    j = pq[1] + neighbours[c][1]
                    if(check_limit(image.shape, i, j)):
                        if(image[i,j] < bg):
                            c = (c + 5)%8
                            border.append((i,j))
                            pq = (i,j)
                            break
                        c = (c + 1)%8
                while(pq != origin):
                    #c_start = c
                    for _ in range(0, 7):
                        i = pq[0] + neighbours[c][0]
                        j = pq[1] + neighbours[c][1]
                        if(not (check_limit(image.shape, i, j))):
                            continue
                        if(image[i,j] < bg):
                            c = (c + 5)%8
                            border.append((i,j))
                            pq = (i,j)
                            break
                        c = (c + 1)%8
                    #if(c_start == c):
                        #break
                a = np.array(border)
                miny = np.min(a[:,0]) - 1
                maxy = np.max(a[:,0]) + 1
                minx = np.min(a[:,1]) - 1
                maxx = np.max(a[:,1]) + 1
                limit = [minx, maxx, miny, maxy]

                if(len(border) > 10):
                    image_color = floodfill(image_copy, border[0][0],border[0][1], bg, limit, image)
                    Image.fromarray(np.uint8(image_color)).save("Imagens/" + name_image + "_" + str(count) + ".png")
                    count = count + 1

                border = []

    Image.fromarray(np.uint8(image_copy)).show()
    #im = Image.fromarray(np.uint8(image))
