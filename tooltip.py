import os
import argparse
from PIL import Image

class vec:
    axis = "xyzw"
    def __init__(self, *args):
        if type(args[0]) in (list, tuple): args = args[0]
        self.points = list(args)
    def __getattr__(self, attr):
        if attr in self.axis:
            return self.points[self.axis.find(attr)]
        return super().getattr(self, attr)

def tohex(color):
    color = (color[0] << 24) + (color[1] << 16) + (color[2] << 8) + (color[3])
    return hex(color) + 'u'
def encode(image, a, b):
    return ','.join([tohex(image.getpixel((x,y))) for y in range(b[0], b[1]) for x in range(a[0], a[1])])

def tooltip(image, corner, pad):
    size = vec(image.size)
    file = open("tooltip.glsl", "w")
    file.write("//generated for tooltip shader by Godlander\n")
    file.write("vec2 pad = vec2(" + str(pad[0]) + "," + str(pad[1]) + ");\n")
    file.write("ivec3 sizes = ivec3(" + str(size.x-corner*2) +"," + str(size.y-corner*2) + "," + str(corner) + ");\n")
    file.write("uint base = " + tohex(image.getpixel((corner, corner))) + ";\n")
    file.write("uint[] tl = uint[](" + encode(image, (0, corner),             (0, corner))             + ");\n")
    file.write("uint[] tr = uint[](" + encode(image, (size.x-corner, size.x), (0, corner))             + ");\n")
    file.write("uint[] bl = uint[](" + encode(image, (0, corner),             (size.y-corner, size.y)) + ");\n")
    file.write("uint[] br = uint[](" + encode(image, (size.x-corner, size.x), (size.y-corner, size.y)) + ");\n")
    file.write("uint[] t = uint[]("  + encode(image, (corner, size.x-corner), (0, corner))             + ");\n")
    file.write("uint[] l = uint[]("  + encode(image, (0, corner),             (corner, size.y-corner)) + ");\n")
    file.write("uint[] r = uint[]("  + encode(image, (size.x-corner, size.x), (corner, size.y-corner)) + ");\n")
    file.write("uint[] b = uint[]("  + encode(image, (corner, size.x-corner), (size.y-corner, size.y)) + ");\n")
    file.close()

path = os.getcwd()
class ArgumentParserError(Exception): pass
class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)
parser = ThrowingArgumentParser(description="python script to generate a tooltip shader from image")
parser.add_argument("--file", type=str, help="Tooltip image file", default='')
parser.add_argument("--corner", type=int, help="Tooltip corner size", default=3)
parser.add_argument("--pad", type=int, nargs=2, help="Tooltip horizontal/vertical padding", default=(0,0))
args = parser.parse_args()
image = Image.open(args.file).convert("RGBA")
tooltip(image, args.corner, args.pad)