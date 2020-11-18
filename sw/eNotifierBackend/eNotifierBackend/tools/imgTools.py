
def reseizeImage(image, newSize):
    width, height = image.size

    newImg = image.crop((0, 0, width, height))
    newImg = newImg.resize(newSize)
    return newImg
