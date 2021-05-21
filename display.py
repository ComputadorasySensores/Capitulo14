import time

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

import subprocess

i2c = busio.I2C(SCL, SDA)

# 128x64 display con hardware I2C:
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Limpia pantalla
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

font = ImageFont.load_default()

while True:

    
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Ref script para monitoreo : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I |cut -c 1-13"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disco: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True )

    draw.text((x, top), "Computadoras", font=font, fill=255)	#Tu texto personalizado 1
    draw.text((x+68, top+7), "y Sensores", font=font, fill=255)	#Tu texto personalizado 2
    draw.text((x, top+28), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((x, top+37), "Temperatura: " + str(temp,'utf-8') , font=font, fill=255)
    draw.text((x, top+46), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((x, top+55), str(Disk,'utf-8'), font=font, fill=255)

    # Muestra imagen.
    disp.image(image)
    disp.show()
    time.sleep(1) # tasa de refresco
