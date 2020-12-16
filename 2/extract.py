import numpy as np
#import cv2 as cv
from PIL import Image


def bar(border, limit):
    """Cria array que representa a subimagem do perimetro"""

    #instancia o array
    new_image = np.zeros((limit[3]-limit[2],limit[1]-limit[0]), dtype=int)

    #preenche com branco
    new_image[:] = 255

    #para cada pixel da borda a posição correspondente do new_image é pintado
    #de preto
    for x in border:
      new_image[x[0] - limit[2],x[1] - limit[0]] = 0
    return new_image

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
  new_image[y - limit[2], x - limit[0]] = image[y,x]
  image_grayscale[y,x] = False

  while(len(q)):
    pos = q[0]
    q.pop(0)

    if(check_limit(image_grayscale.shape, pos[0], pos[1] + 1) and image_grayscale[pos[0],pos[1]+1] ):
      q.append((pos[0],pos[1]+1))
      new_image[pos[0] - limit[2], pos[1]+1 - limit[0]] = image[pos[0],pos[1]+1]
      image_grayscale[pos[0],pos[1]+1] = False

    if(check_limit(image_grayscale.shape, pos[0], pos[1] - 1) and image_grayscale[pos[0],pos[1]-1] ):
      q.append((pos[0],pos[1]-1))
      new_image[pos[0] - limit[2], pos[1]-1 - limit[0]] = image[pos[0],pos[1]-1]
      image_grayscale[pos[0],pos[1]-1] = False

    if(check_limit(image_grayscale.shape, pos[0] - 1, pos[1]) and image_grayscale[pos[0]-1,pos[1]] ):
      q.append((pos[0]-1,pos[1]))
      new_image[pos[0]-1 - limit[2], pos[1] - limit[0]] = image[pos[0]-1,pos[1]]
      image_grayscale[pos[0]-1,pos[1]] = False

    if(check_limit(image_grayscale.shape, pos[0] + 1, pos[1]) and image_grayscale[pos[0]+1,pos[1]] ):
      q.append((pos[0]+1,pos[1]))
      new_image[pos[0]+1 - limit[2], pos[1] - limit[0]] =  image[pos[0]+1,pos[1]]
      image_grayscale[pos[0]+1,pos[1]] = False

    if(check_limit(image_grayscale.shape, pos[0] + 1, pos[1] + 1) and image_grayscale[pos[0]+1,pos[1]+1] ):
      q.append((pos[0]+1,pos[1]+1))
      new_image[pos[0]+1 - limit[2], pos[1]+1 - limit[0]] = image[pos[0]+1,pos[1]+1]
      image_grayscale[pos[0]+1,pos[1]+1] = False

    if(check_limit(image_grayscale.shape, pos[0] - 1, pos[1] - 1) and image_grayscale[pos[0]-1,pos[1]-1] ):
      q.append((pos[0]-1,pos[1]-1))
      new_image[pos[0]-1 - limit[2], pos[1]-1 - limit[0]] = image[pos[0]-1,pos[1]-1]
      image_grayscale[pos[0]-1,pos[1]-1] = False

    if(check_limit(image_grayscale.shape, pos[0] - 1, pos[1] + 1) and image_grayscale[pos[0]-1,pos[1]+1] ):
      q.append((pos[0]-1,pos[1]+1))
      new_image[pos[0]-1 - limit[2], pos[1]+1 - limit[0]] = image[pos[0]-1,pos[1]+1]
      image_grayscale[pos[0]-1,pos[1]+1] = False

    if(check_limit(image_grayscale.shape, pos[0] + 1, pos[1] - 1) and image_grayscale[pos[0]+1,pos[1]-1] ):
      q.append((pos[0]+1,pos[1]-1))
      new_image[pos[0]+1 - limit[2], pos[1]-1 - limit[0]] =  image[pos[0]+1,pos[1]-1]
      image_grayscale[pos[0]+1,pos[1]-1] = False
  return new_image

def foo(file):
    name_image = file[7:-4]

    im = Image.open(file)
    if(im.mode == "RGBA"):
        im.putalpha(255)
        #print(im.getpixel((0,0)))
        
    im = im.convert("RGB")

    #print(len(im.mode))
    #exit()

    bg = 220
    neighbours = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]]

    border = []

    image_copy = np.array(im)

    image_l = np.array(im.convert("L"))

    height = image_l.shape[0]
    width = image_l.shape[1]

    image_l = np.where(image_l > bg, image_l, True)
    image_l = np.where(image_l < bg, image_l, False)

    image = np.array(image_l, dtype=bool)

    #kernel = np.ones((5,5),np.uint8)
    #image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)

    count = 0

    for x in range(0,height):
      for y in range(0,width):
          if(image[x,y]):
                origin = pq = (x,y)
                c = 0
                border.append((x,y))
                for _ in range(0, 7):
                    i = pq[0] + neighbours[c][0]
                    j = pq[1] + neighbours[c][1]
                    if(check_limit(image.shape, i, j)):
                        if(image[i,j]):
                            c = (c + 5)%8
                            border.append((i,j))
                            pq = (i,j)
                            break
                    c = (c + 1)%8
                while(pq != origin):
                    #start_pq = pq
                    for _ in range(0, 7):
                        i = pq[0] + neighbours[c][0]
                        j = pq[1] + neighbours[c][1]
                        if(not (check_limit(image.shape, i, j))):
                            c = (c + 1)%8
                            continue
                        if(image[i,j]):
                            c = (c + 5)%8
                            border.append((i,j))
                            pq = (i,j)
                            break
                        c = (c + 1)%8
                    #if(start_pq[0] == pq[0] and start_pq[1] == pq[1]):
                        #print(start_pq, pq)
                        #break
                a = np.array(border)
                miny = np.min(a[:,0]) - 1
                maxy = np.max(a[:,0]) + 1
                minx = np.min(a[:,1]) - 1
                maxx = np.max(a[:,1]) + 1
                limit = [minx, maxx, miny, maxy]
                meanf = np.mean(a, axis=0)
                meani = (int(meanf[0] - miny), int(meanf[1] - minx))
                #print(meani)

                if(len(border) > 20):
                    image_color = floodfill(image_copy, border[0][0],border[0][1], bg, limit, image)
                    image_p = bar(border,limit)
                    #image_p[meani] = 0
                    name_file = "Imagens/" + name_image + "_" + str(count) + ".png"
                    name_filep = "Imagens/" + name_image + "_" + str(count)+ '-P' + ".png"
                    Image.fromarray(np.uint8(image_color)).save(name_file)
                    Image.fromarray(np.uint8(image_p)).save(name_filep)
                    count = count + 1

                border = []

    #Image.fromarray(np.uint8(image_copy)).show()
    #im = Image.fromarray(np.uint8(image))
