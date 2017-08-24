from PIL import Image
import math
def image_entropy(img):
    """calculate the entropy of an image"""
    hist = img.histogram()
    hist_size = sum(hist)
    hist = [float(h) / hist_size for h in hist]

    return -sum([p * math.log(p, 2) for p in hist if p != 0])

def image_square(img):
    """if the image is taller than it is wide, square it off. determine
    which pieces to cut off based on the entropy pieces."""
    x,y = img.size
    while y > x:
        #slice 10px at a time until square
        slice_height = min(y - x, 5)

        bottom = img.crop((0, y - slice_height, x, y))
        top = img.crop((0, 0, x, slice_height))

        #remove the slice with the least entropy
        if image_entropy(bottom) < image_entropy(top):
            img = img.crop((0, 0, x, y - slice_height))
        else:
            img = img.crop((0, slice_height, x, y))

        x,y = img.size

    while x > y:
        slice_width = min(x - y, 5)
        left = img.crop((0, 0, slice_width, y))
        right = img.crop((x - slice_width, 0, x, y))
        if image_entropy(left) < image_entropy(right):
            img = img.crop((slice_width, 0, x, y))
        else:
            img = img.crop((0, 0, x - slice_width, y))
        x,y = img.size

    return img

#img = Image.open('test.png')
#img1 = image_square(img)
#img1.save('test.cropped.png')

