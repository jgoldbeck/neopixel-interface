#!/usr/bin/python
import Image
im = Image.open('greengradhor.png').convert('RGB')
print im.getbands()
# print pixels[255,255] # x, y
strip = im.crop((0,0,1,255))
width = strip.size[0]
height = strip.size[1]
print width
print height
pixel_strip = im.load()
pixel_list = [pixel_strip[x, 0] for x in range(height)]
print pixel_list


gamma = bytearray(256)
for i in range(256):
    gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

column = [0 for x in range(width)]
column = bytearray(height * 3 + 1)

for y in range(height):
    value = pixel_list[y]
    y3 = y * 3
    column[y3]     = gamma[value[1]]
    column[y3 + 1] = gamma[value[0]]
    column[y3 + 2] = gamma[value[2]]
for y in range(height*3):
    print chr(column[y])
