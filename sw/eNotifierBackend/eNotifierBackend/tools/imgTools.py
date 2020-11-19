from PIL import Image


def reseizeImage(image, newSize):
    width, height = image.size

    newImg = image.crop((0, 0, width, height))
    newImg = newImg.resize(newSize)
    return newImg

def rotateImage(img, degree):
    degree = 360 - degree
    # converted to have an alpha layer
    im2 = img.convert('RGBA')
    # rotated image
    rot = im2.rotate(degree, expand=1)
    # a white image same size as rotated image
    fff = Image.new('RGBA', rot.size, (255,) * 4)
    # create a composite image using the alpha layer of rot as a mask
    out = Image.composite(rot, fff, rot)
    # save your work (converting back to mode='1' or whatever..)
    return out.convert(img.mode)
