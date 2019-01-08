#!/usr/bin/env python
"""
Pack multiple images of different sizes into one image.

Based on S W's recipe:
http://code.activestate.com/recipes/442299/
http://code.activestate.com/recipes/578585/
Licensed under the PSF License
"""
from __future__ import print_function
import argparse
import glob
from PIL import Image, ImageChops
import os
import math
# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing
    assert timing  # silence warnings
except ImportError:
    pass

def resize(d,dimensions):
    #Only works for square dimensions
    d=d
    dimensions=dimensions
    if not os.path.exists("resized images"):
        os.makedirs("resized images")
    if not os.path.exists("cropped images"):
        os.makedirs("cropped images")
    try:
        files = os.listdir(os.path.join(os.getcwd(),"source images"))
    except IOError:
        print('No folder found.')
        input('Enter any key to exit: ')
        exit()
    
    xDimension=dimensions[0]
    yDimension=dimensions[1]
    print(xDimension)
    print(yDimension)
    totalViews=0
    for item in d:
        totalViews+=d[item]
    files.sort()
    for index, file in enumerate(files):
        path = os.path.join(os.getcwd(), "source images", file)
        filename=int(file.split('.')[0])
        trim(path, file)
        img = Image.open("cropped images/"+file)
        ratio=(d[filename]/totalViews)
        resizedX=int(math.ceil(math.sqrt((xDimension*yDimension*ratio))))
        resizedY=int(.75*math.ceil(math.sqrt((xDimension*yDimension*ratio))))
        resized=img.resize((resizedX, resizedY))
        resized.save("resized images/"+str(filename)+".jpg", 'JPEG')

def trim(path, file):
    path=path
    file=file
    im=Image.open(path)
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im= im.crop(bbox)
    im.save("cropped images/"+file, "JPEG")

"""     
def extract(path, file):
    path=path
    file=file
    #== Parameters =======================================================================
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,1.0) # In BGR format


    #== Processing =======================================================================

    #-- Read image -----------------------------------------------------------------------
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    cv2.imshow('img', masked)                                   # Display
    cv2.waitKey()

        # split image into channels
    c_red, c_green, c_blue = cv2.split(img)

    # merge with mask got on one of a previous steps
    img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))

    # save to disk
    filename=(file.split('.')[0])
    cv2.imwrite(filename+'.jpg', img_a*255)
    print('Extracted background from file '+filename)
    #cv2.imwrite('C:/Temp/person-masked.jpg', masked)           # Save
"""
def tuple_arg(s):
    try:
        if ',' in s:
            w, h = map(int, s.split(','))
        elif ':' in s:
            w, h = map(int, s.split(':'))
        elif 'x' in s:
            w, h = map(int, s.split('x'))
        return w, h
    except:
        raise argparse.ArgumentTypeError("Value must be w,h or w:h or wxh")


class PackNode(object):
    """
    Creates an area which can recursively pack other areas of smaller sizes into itself.
    """
    def __init__(self, area):
        #if tuple contains two elements, assume they are width and height, and origin is (0,0)
        if len(area) == 2:
            area = (0,0,area[0],area[1])
        self.area = area

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.area))

    def get_width(self):
        return self.area[2] - self.area[0]
    width = property(fget=get_width)

    def get_height(self):
        return self.area[3] - self.area[1]
    height = property(fget=get_height)

    def insert(self, area):
        if hasattr(self, 'child'):
            a = self.child[0].insert(area)
            if a is None: return self.child[1].insert(area)
            return a

        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [None,None]
            self.child[0] = PackNode((self.area[0]+area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1]+area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0]+area.width, self.area[1]+area.height))

def run(dimensions):
    parser = argparse.ArgumentParser(
        description='Pack multiple images of different sizes into one image.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--inspec', default='resized images/*.jpg',
        help='Input file spec')
    parser.add_argument(
        '-o', '--outfile', default='sizedComposite.png',
        help='Output image file')
    parser.add_argument(
        '-s', '--size', type=tuple_arg, metavar='pixels',
        help="Size (width,height tuple) of the image we're packing into",
        default="2160,2160")
    parser.add_argument(
        '-l', '--largest_first', action='store_true',
        help='Pack largest images first')
    parser.add_argument(
        '-t', '--tempfiles', action='store_true',
        help='Save temporary files to show filling')
    args = parser.parse_args()
    args.largest_first=True
    args.tempfiles=True
    dimensions=dimensions
    args.size=dimensions
    print(dimensions)

    im_format = 'RGBA'
    #get a list of PNG files in the current directory
    names = glob.glob(args.inspec)
    if args.outfile in names:
        names.remove(args.outfile)  # don't include any pre-existing output

    #create a list of PIL Image objects, sorted by size
    print("Create a list of PIL Image objects, sorted by size")
    images = sorted([(i.size[0]*i.size[1], name, i) for name, i in ((x, Image.open(x).convert(im_format)) for x in names)], reverse=args.largest_first)

    print("Create tree")
    tree = PackNode(args.size)
    image = Image.new(im_format, args.size)

    #insert each image into the PackNode area
    for i, (area, name, img) in enumerate(images):
        print(name, img.size)
        uv = tree.insert(img.size)
        if uv is None:
            raise ValueError(
                'Pack size ' + str(args.size) + ' too small, cannot insert ' +
                str(img.size) + ' image.')
        image.paste(img, uv.area)
        if not os.path.exists("temp pack images"):
            os.makedirs("temp pack images")
        if args.tempfiles:
            image.save("temp pack images/temp" + str(i).zfill(4) + ".png")

    image.save(args.outfile)
    image.show()

# End of file