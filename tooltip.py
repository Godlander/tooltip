from pathlib import Path
import argparse
from PIL import Image

CURRENT_FILE = Path(__file__).parent


class Vec:
    axis = "xyzw"

    def __init__(self, *args):
        if type(args[0]) in (list, tuple):
            args = args[0]
        self.points = list(args)

    def __getattr__(self, attr):
        if attr in self.axis:
            return self.points[self.axis.find(attr)]
        return super().getattr(self, attr)


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def toHex(color) -> str:
    color = (color[0] << 24) + (color[1] << 16) + (color[2] << 8) + (color[3])
    return hex(color) + "u"


def encode(image: Image, a: tuple[int, int], b: tuple[int, int]) -> str:
    return ",".join(
        [
            toHex(image.getpixel((x, y)))
            for y in range(b[0], b[1])
            for x in range(a[0], a[1])
        ]
    )


def tooltip(image: Image, corner: int, pad: int):
    size = Vec(image.size)
    lines = [
        "//generated for tooltip shader by Godlander",
        f"vec2 pad = vec2({pad[0]},{pad[1]});",
        f"ivec3 sizes = ivec3({size.x-corner*2},{size.y-corner*2},{corner});",
        f"uint base = {toHex(image.getpixel((corner, corner)))};",
        f"uint[] tl = uint[]({encode(image, (0, corner),             (0, corner))            });",
        f"uint[] tr = uint[]({encode(image, (size.x-corner, size.x), (0, corner))            });",
        f"uint[] bl = uint[]({encode(image, (0, corner),             (size.y-corner, size.y))});",
        f"uint[] br = uint[]({encode(image, (size.x-corner, size.x), (size.y-corner, size.y))});",
        f"uint[] t = uint[]({ encode(image, (corner, size.x-corner), (0, corner))            });",
        f"uint[] l = uint[]({ encode(image, (0, corner),             (corner, size.y-corner))});",
        f"uint[] r = uint[]({ encode(image, (size.x-corner, size.x), (corner, size.y-corner))});",
        f"uint[] b = uint[]({ encode(image, (corner, size.x-corner), (size.y-corner, size.y))});",
    ]
    with open(CURRENT_FILE / "tooltip.glsl", "w") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    parser = ThrowingArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="python script to generate a tooltip shader from image",
    )
    parser.add_argument("--file", type=str, help="Tooltip image file", default="")
    parser.add_argument("--corner", type=int, help="Tooltip corner size", default=3)
    parser.add_argument(
        "--pad",
        type=int,
        nargs=2,
        help="Tooltip horizontal/vertical padding",
        default=(0, 0),
    )
    args = parser.parse_args()
    with Image.open(CURRENT_FILE / args.file) as img:
        img = img.convert("RGBA")
        tooltip(img, args.corner, args.pad)
