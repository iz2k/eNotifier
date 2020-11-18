#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from PIL import Image,ImageDraw,ImageFont

from epaper.epd75bv2.epdCtl import epdCtl

def reseizeImage(image, newSize):
    width, height = image.size

    newImg = image.crop((0, 0, width, height))
    newImg = newImg.resize(newSize)
    return newImg

def menu():
    print('1 - Clear display')
    print('2 - Load coded image')
    print('3 - Load BMP')
    print('4 - Load BMP on window')
    print('5 - Homescreen sample')
    print('q - Quit')

def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    picdir = 'pic'

    try:

        epd = epdCtl()
        font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        run=True

        while(run):
            menu()
            opt=input('Select option: ')
            if (opt == '1'):
                epd.clear()
            if (opt == '2'):
                imageBlack = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                imageRed = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                drawBlack = ImageDraw.Draw(imageBlack)
                drawRed = ImageDraw.Draw(imageRed)
                drawBlack.text((10, 0), 'hello world', font = font24, fill = 0)
                drawBlack.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
                drawBlack.text((150, 0), u'微雪电子', font = font24, fill = 0)
                drawRed.line((20, 50, 70, 100), fill = 0)
                drawRed.line((70, 50, 20, 100), fill = 0)
                drawRed.rectangle((20, 50, 70, 100), outline = 0)
                drawRed.line((165, 50, 165, 100), fill = 0)
                drawBlack.line((140, 75, 190, 75), fill = 0)
                drawBlack.arc((140, 50, 190, 100), 0, 360, fill = 0)
                drawBlack.rectangle((80, 50, 130, 100), fill = 0)
                drawBlack.chord((200, 50, 250, 100), 0, 360, fill = 0)
                epd.display(imageBlack,imageRed)
            if (opt == '3'):
                imageBlack = Image.open(os.path.join(picdir, '7in5_V2_b.bmp'))
                imageRed = Image.open(os.path.join(picdir, '7in5_V2_r.bmp'))
                epd.display(imageBlack,imageRed)
            if (opt == '4'):
                imageBlack = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                imageRed = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
                imageBlack.paste(bmp, (50,10))
                imageRed.paste(bmp, (50,300))
                epd.display(imageBlack,imageRed)
            if (opt == '5'):
                imageBlack = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                imageRed = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                drawBlack = ImageDraw.Draw(imageBlack)
                drawRed = ImageDraw.Draw(imageRed)

                imageRed.paste(Image.open(os.path.join(picdir, 'home.png'))
                                 , (30,30))
                drawBlack.text((110, 38), 'Etxean', font = font48, fill = 0)

                imageBlack.paste(Image.open(os.path.join(picdir, 'thermo.png'))
                                 , (50,130))
                drawRed.text((130, 138), '25.6ºC', font = font48, fill = 0)

                imageBlack.paste(Image.open(os.path.join(picdir, 'hygro.png'))
                                 , (50,210))
                drawRed.text((130, 218), '58%', font = font48, fill = 0)

                imageBlack.paste(Image.open(os.path.join(picdir, 'pressure.png'))
                                 , (50,290))
                drawRed.text((130, 298), '1002mb', font = font48, fill = 0)

                imageBlack.paste(Image.open(os.path.join(picdir, 'air.png'))
                                 , (50,370))
                drawRed.text((130, 378), '32', font = font48, fill = 0)


                imageBlack.paste(Image.open(os.path.join(picdir, 'city.png'))
                                 , (700,30))
                drawRed.text((460, 38), 'Donostian', font = font48, fill = 0)

                imageBlack.paste(Image.open(os.path.join(picdir, 'weather/03-partly-cloudy-day.png'))
                                 , (520,120))

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'thermo.png')), (32, 32))
                                 , (450,270))
                drawBlack.text((490, 274), '21.1ºC', font = font24, fill = 0)

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'pressure.png')), (32, 32))
                                 , (600,270))
                drawBlack.text((640, 274), '1008mb', font = font24, fill = 0)

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'hygro.png')), (32, 32))
                                 , (450,320))
                drawBlack.text((490, 324), '63%', font = font24, fill = 0)

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'air.png')), (32, 32))
                                 , (600,320))
                drawBlack.text((640, 324), '39', font = font24, fill = 0)

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'wind.png')), (32, 32))
                                 , (450,370))
                drawBlack.text((490, 374), '20km/h', font = font24, fill = 0)

                imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'rain.png')), (32, 32))
                                 , (600,370))
                drawBlack.text((640, 374), '20%', font = font24, fill = 0)

                drawBlack.rectangle((490, 440, 800, 480), fill = 0)
                drawBlack.polygon([(490, 440), (490, 480), (460, 480)], fill = 0)
                drawBlack.text((500, 445), 'Azken neurketa:', font = font24, fill = 1)
                drawRed.text((700, 445), '16:15', font = font24, fill = 0)

                epd.display(imageBlack,imageRed)

            if (opt == 'q'):
                epd.sleep()
                run = False

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.epdconfig._module_exit()
        exit()

# If executed as main, call main
if __name__ == "__main__":
    main(sys.argv)
