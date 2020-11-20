import os

from PIL import ImageFont, Image, ImageDraw

from eNotifierBackend.tools.imgTools import reseizeImage, rotateImage
from eNotifierBackend.tools.timeTools import getDateTime


def weatherHomeScreen(epd, weatherReport, sensorReport):
    print('Updating HomeScreen')
    picdir = 'pic'
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    imageBlack = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
    imageRed = Image.new('1', (epd.SCREEN_WIDTH, epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
    drawBlack = ImageDraw.Draw(imageBlack)
    drawRed = ImageDraw.Draw(imageRed)

    imageRed.paste(Image.open(os.path.join(picdir, 'home.png'))
                   , (30, 30))
    drawBlack.text((110, 38), 'Etxean', font=font48, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'thermo.png'))
                     , (50, 130))
    drawRed.text((130, 138), str(sensorReport['temperature']) + 'ºC', font=font48, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'hygro.png'))
                     , (50, 210))
    drawRed.text((130, 218), str(round(sensorReport['humidity'], 1)) + '%', font=font48, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'pressure.png'))
                     , (50, 290))
    drawRed.text((130, 298), str(round(sensorReport['pressure'])) + 'mb', font=font48, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'air.png'))
                     , (50, 387))
    drawBlack.text((130, 385), 'eCO2', font=font24, fill=0)
    drawRed.text((200, 375), str(round(sensorReport['eCO2'])) + 'ppm', font=font36, fill=0)
    drawBlack.text((130, 420), 'TVOC', font=font24, fill=0)
    drawRed.text((200, 418), str(round(sensorReport['TVOC'])) + 'ppb', font=font36, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'city.png'))
                     , (700, 30))
    drawRed.text((460, 38), 'Donostian', font=font48, fill=0)

    imageBlack.paste(Image.open(os.path.join(picdir, 'weather/' + weatherReport['current']['weather'][0]['icon'] + '.png'))
                     , (535, 120))

    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'thermo.png')), (32, 32))
                   , (450, 270))
    drawBlack.text((490, 274), str(weatherReport['current']['temp']) + 'ºC', font=font24, fill=0)

    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'pressure.png')), (32, 32))
                   , (630, 270))
    drawBlack.text((670, 274), str(weatherReport['current']['pressure']) + 'mb', font=font24, fill=0)

    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'hygro.png')), (32, 32))
                   , (450, 320))
    drawBlack.text((490, 324), str(weatherReport['current']['humidity']) + '%', font=font24, fill=0)

    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'sunbath.png')), (32, 32))
                   , (630, 320))
    drawBlack.text((670, 324),  str(weatherReport['current']['uvi']) + 'uv', font=font24, fill=0)

    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'wind.png')), (32, 32))
                   , (450, 370))
    wind_source = weatherReport['current']['wind_deg']
    wind_direction = wind_source + 180
    imageBlack.paste(rotateImage(reseizeImage(Image.open(os.path.join(picdir, 'arrow.png')), (20, 20)), wind_direction)
                   , (484, 374))

    drawBlack.text((510, 374), str(int(round(weatherReport['current']['wind_speed'] * 3.6))) + 'km/h', font=font24, fill=0)


    imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'rain.png')), (32, 32))
                   , (630, 370))
    drawBlack.text((670, 374), str(weatherReport['hourly'][0]['pop'] * 100) + '%', font=font24, fill=0)

    drawBlack.rectangle((490, 440, 800, 480), fill=0)
    drawBlack.polygon([(490, 440), (490, 480), (460, 480)], fill=0)
    drawRed.text((500, 445), 'Azken neurketa:', font=font24, fill=0)
    date = getDateTime()
    date_String = str(date['hour']) + ':' + str(date['minute']).zfill(2)
    drawBlack.text((700, 445), date_String, font=font24, fill=1)

    epd.display(imageBlack, imageRed)
