import argparse
import logging
import re
from collections import defaultdict
from enum import Enum
from itertools import zip_longest
from typing import List, Mapping, Sequence, Iterator, Optional

LOG = logging.getLogger(__name__)


class Pixel(Enum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


class SIF:
    def __init__(self, data: str, width: int, height: int) -> None:
        self.layers: List[Sequence[Sequence[Pixel]]] = []
        self.width = width
        self.height = height
        idx = 0
        while idx < len(data):
            layer = []
            for y in range(height):
                layer.append([Pixel(int(value)) for value in data[idx + y*width:idx + (y+1)*width]])
            self.layers.append(layer)
            idx += width * height

    def flattened(self) -> Sequence[Sequence[Pixel]]:
        canvas = [row[:] for row in [[Pixel.TRANSPARENT] * self.width] * self.height]
        for layer in reversed(self.layers):
            for y in range(self.height):
                for x in range(self.width):
                    pixel = Pixel(layer[y][x])
                    if pixel != Pixel.TRANSPARENT:
                        canvas[y][x] = pixel
        return canvas


def layer_count(layer: Sequence[Sequence[Pixel]], value: int) -> int:
    return sum(row.count(Pixel(value)) for row in layer)


def layer_str(layer: Sequence[Sequence[Pixel]]) -> str:
    ret = ''
    for row in layer:
        ret += ''.join(str(val.value) for val in row) + '\n'
    return ret


def layer_draw(layer: Sequence[Sequence[Pixel]]) -> str:
    return layer_str(layer).translate(str.maketrans({
        str(Pixel.TRANSPARENT.value): 'X',
        str(Pixel.BLACK.value): '\u0020',
        str(Pixel.WHITE.value): '\u2588',
    }))


def parta(data: str, width: int = 25, height: int = 6) -> int:
    sif = SIF(data=data, width=width, height=height)
    layer = sorted(sif.layers, key=lambda layer: layer_count(layer, 0))[0]

    LOG.debug('Layer: \n%s', layer_str(layer))
    return layer_count(layer, 1) * layer_count(layer, 2)


def partb(data: str, width: int = 25, height: int = 6) -> str:
    sif = SIF(data=data, width=width, height=height)
    for idx in range(len(sif.layers)):
        LOG.debug('Layer %s: \n%s', idx, layer_draw(sif.layers[idx]))
    return layer_draw(sif.flattened())


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day8.txt')
    args = parser.parse_args()
    input_data = args.infile.read().strip()
    print(parta(input_data))
    print(partb(input_data))
