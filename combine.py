import os

from PIL import Image
import math


def equalSizedComposite():
    try:
        files = os.listdir(os.path.join(os.getcwd(),"source images"))
    except IOError:
        print('No folder found.')
        input('Enter any key to exit: ')
        exit()

    result = Image.new("RGB", (1080, 1080))
    try:
        rows=math.floor(math.sqrt(len(files)))
        columns=((len(files))+(rows-1))//rows
        xCount=0
        yCount=0
    except ZeroDivisionError:
        print('No video thumbnails found in source images folder.')

    for index, file in enumerate(files):
        path = os.path.join(os.getcwd(), "source images", file)
        img = Image.open(path)
        xDimension=1080//columns
        """((len(files)+1)//2)"""
        yDimension=1080//rows
        w, h = img.size
        if w==1920:
            img=img.crop(box=(840,0,1920,1080))
        img=img.resize((xDimension, yDimension))
        x = index % columns * xDimension
        y = yCount * yDimension
        xCount+=1
        if xCount==columns:
            yCount+=1
            xCount=0
        w = xDimension
        h = yDimension
        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))

    result.save('equalSizedComposite.jpg')