#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image,ImageDraw,ImageFont

from epaper.epd75bv2.epdCtl import epdCtl

def menu():
    print('1 - Clear display')
    print('2 - Load coded image')
    print('3 - Load BMP')
    print('4 - Load BMP on window')
    print('q - Quit')

def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    picdir = 'pic'

    try:

        epd = epdCtl()
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        run=True

        while(run):
            menu()
            opt=input('Select option: ')
            if (opt == '1'):
                epd.clear()
            if (opt == '2'):
                Himage = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                Other = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
                draw_Himage = ImageDraw.Draw(Himage)
                draw_other = ImageDraw.Draw(Other)
                draw_Himage.text((10, 0), 'hello world', font = font24, fill = 0)
                draw_Himage.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
                draw_Himage.text((150, 0), u'微雪电子', font = font24, fill = 0)
                draw_other.line((20, 50, 70, 100), fill = 0)
                draw_other.line((70, 50, 20, 100), fill = 0)
                draw_other.rectangle((20, 50, 70, 100), outline = 0)
                draw_other.line((165, 50, 165, 100), fill = 0)
                draw_Himage.line((140, 75, 190, 75), fill = 0)
                draw_Himage.arc((140, 50, 190, 100), 0, 360, fill = 0)
                draw_Himage.rectangle((80, 50, 130, 100), fill = 0)
                draw_Himage.chord((200, 50, 250, 100), 0, 360, fill = 0)
                epd.display(Himage,Other)
            if (opt == '3'):
                Himage = Image.open(os.path.join(picdir, '7in5_V2_r.bmp'))
                Himage_Other = Image.open(os.path.join(picdir, '7in5_V2_b.bmp'))
                epd.display(Himage,Himage_Other)
            if (opt == '4'):
                Himage2 = Image.new('1', (epd.SCREEN_HEIGHT, epd.SCREEN_WIDTH), 255)  # 255: clear the frame
                Himage2_Other = Image.new('1', (epd.SCREEN_HEIGHT, epd.SCREEN_WIDTH), 255)  # 255: clear the frame
                bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
                Himage2.paste(bmp, (50,10))
                Himage2_Other.paste(bmp, (50,300))
                epd.display(Himage2, Himage2_Other)
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
