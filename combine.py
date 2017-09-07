from __future__ import print_function
import os

from PIL import Image
import math

def combine():
    files = os.listdir(os.path.join(os.getcwd(),"Playlist images"))

    result = Image.new("RGB", (1080, 1080))

    rows=math.floor(math.sqrt(len(files)))
    columns=((len(files))+(rows-1))//rows

    for index, file in enumerate(files):
        path = os.path.join(os.getcwd(), "Playlist images", file)
        img = Image.open(path)
        xDimension=1080//columns
        """((len(files)+1)//2)"""
        yDimension=1080//rows
        w, h = img.size
        if w==1920:
            img=img.crop(box=(840,0,1920,1080))
        img=img.resize((xDimension, yDimension))
        x = index % columns * xDimension
        y = index % rows * yDimension
        w = xDimension
        h = yDimension
        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))

    result.save('PlaylistComposite.jpg')


combine()