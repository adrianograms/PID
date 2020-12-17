import numpy as np
import cv2 as cv
from PIL import Image


def bar(border, limit):
    """Cria array que representa a subimagem do perimetro"""

    #instancia o array
    new_image = np.zeros((limit[3]-limit[2],limit[1]-limit[0]), dtype=int)

    #preenche com branco
    new_image[:] = 255

    a_p = []

    #para cada pixel da borda a posição correspondente do new_image é pintado
    #de preto
    for x in border:
      a_p.append((x[0] - limit[2],x[1] - limit[0]))
      new_image[x[0] - limit[2],x[1] - limit[0]] = 0
    return new_image, np.array(a_p)

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

def baz(a, image):
    meanf = np.mean(a, axis=0)
    y0,x0 = int(meanf[0]), int(meanf[1])

    neighbours = [[-1,-1], [-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1]]

    miny = np.min(a[:,0])
    maxy = np.max(a[:,0])
    minx = np.min(a[:,1])
    maxx = np.max(a[:,1])

    signs = []

    for angle in range(360):
        if(angle <= 45 or angle >= 315):
            for x in range(maxx,x0-1,-1):
                y = int((np.tan(np.radians(angle)) * (x - x0) + y0))
                #print(f"{y} {x}")
                #print(x,y)
                if(not check_limit(image.shape,y,x)):
                    continue
                if(image[y,x] == 0):
                    d = (x0-x)**2 + (y0-y)**2
                    signs.append(d)
                    break
                #codigo novo
                up = y - 1
                up = up if y >= 0 else 0
                down = y + 1
                down = down if y < image.shape[0] else image.shape[0] - 1
                left = x -1
                left = left if x >=0 else 0
                right = x + 1
                right = right if x < image.shape[1] else image.shape[1] - 1
                zeroes = np.argwhere(image[up:down + 1, left:right + 1] == 0)
                if(len(zeroes) > 0):
                    newy = up + zeroes[0][0]
                    nexy = left + zeroes[0][1]
                    d = (x0-nexy)**2 + (y0-newy)**2
                    signs.append(d)
                    break
                #fim codigo novo
                image[y,x] = 127
        elif(angle > 45 and angle <= 135):
            for y in range(0,y0-1,1):
                x = int((1/np.tan(np.radians(-angle)) * (y - y0) + x0))
                #print(f"{y} {x}")
                if(not check_limit(image.shape,y,x)):
                    continue
                if(image[y,x] == 0):
                    d = (x0-x)**2 + (y0-y)**2
                    signs.append(d)
                    break
                #codigo novo
                up = y - 1
                up = up if y >= 0 else 0
                down = y + 1
                down = down if y < image.shape[0] else image.shape[0] - 1
                left = x -1
                left = left if x >=0 else 0
                right = x + 1
                right = right if x < image.shape[1] else image.shape[1] - 1
                zeroes = np.argwhere(image[up:down + 1, left:right + 1] == 0)
                if(len(zeroes) > 0):
                    newy = up + zeroes[0][0]
                    nexy = left + zeroes[0][1]
                    d = (x0-nexy)**2 + (y0-newy)**2
                    signs.append(d)
                    break
                #fim codigo novo
                image[y,x] = 127
        elif(angle >= 225 and angle < 315):
            for y in range(maxy,y0-1,-1):
                x = int((1/np.tan(np.radians(-angle)) * (y - y0) + x0))
                #print(f"{y} {x}")
                if(not check_limit(image.shape,y,x)):
                    continue
                if(image[y,x] == 0):
                    d = (x0-x)**2 + (y0-y)**2
                    signs.append(d)
                    break
                #codigo novo
                up = y - 1
                up = up if y >= 0 else 0
                down = y + 1
                down = down if y < image.shape[0] else image.shape[0] - 1
                left = x -1
                left = left if x >=0 else 0
                right = x + 1
                right = right if x < image.shape[1] else image.shape[1] - 1
                zeroes = np.argwhere(image[up:down + 1, left:right + 1] == 0)
                if(len(zeroes) > 0):
                    newy = up + zeroes[0][0]
                    nexy = left + zeroes[0][1]
                    d = (x0-nexy)**2 + (y0-newy)**2
                    signs.append(d)
                    break
                #fim codigo novo
                image[y,x] = 127

        else:
            for x in range(0,x0+1,1):
                y = int((np.tan(np.radians(angle)) * (x - x0) + y0))
                if(not check_limit(image.shape,y,x)):
                    continue
                if(image[y,x] == 0):
                    d = (x0-x)**2 + (y0-y)**2
                    signs.append(d)
                    break
                #codigo novo
                up = y - 1
                up = up if y >= 0 else 0
                down = y + 1
                down = down if y < image.shape[0] else image.shape[0] - 1
                left = x -1
                left = left if x >=0 else 0
                right = x + 1
                right = right if x < image.shape[1] else image.shape[1] - 1
                zeroes = np.argwhere(image[up:down + 1, left:right + 1] == 0)
                if(len(zeroes) > 0):
                    newy = up + zeroes[0][0]
                    nexy = left + zeroes[0][1]
                    d = (x0-nexy)**2 + (y0-newy)**2
                    signs.append(d)
                    break
                #fim codigo novo
                image[y,x] = 127

    return signs




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

                #print(meani)

                if(len(border) > 20):
                    image_color = floodfill(image_copy, border[0][0],border[0][1], bg, limit, image)
                    image_p,a_p = bar(border,limit)
                    signatures = baz(a_p,image_p)
                    name_file = "Imagens/" + name_image + "_" + str(count) + ".png"
                    name_filep = "Imagens/" + name_image + "_" + str(count)+ '-P' + ".png"
                    Image.fromarray(np.uint8(image_color)).save(name_file)
                    Image.fromarray(np.uint8(image_p)).save(name_filep)
                    print(len(signatures))
                    #Image.fromarray(np.uint8(image_p)).save("a.png")
                    #exit()
                    #image_p[meani] = 0


                    count = count + 1

                border = []
    #Image.fromarray(np.uint8(image_copy)).show()
    #im = Image.fromarray(np.uint8(image))
