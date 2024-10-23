import struct
from enum import IntEnum
from typing import Tuple, Dict, BinaryIO

class ColorDepth(IntEnum):
    RGBA = 32
    GRAYSCALE = 16
    INDEXED = 8

def read_header(filepath: str) -> Tuple[Dict, BinaryIO]:
    """
    Read and parse the header of an Aseprite file.

    Args:
        filepath: Path to .ase/.aseprite file

    Returns:
        tuple: (header dict, file object positioned at first frame)
    """
    f = open(filepath, 'rb')
    try:
        header = {}

        header['file_size'] = struct.unpack('<I', f.read(4))[0]

        magic = struct.unpack('<H', f.read(2))[0]
        if magic != 0xA5E0:
            raise ValueError(f"Invalid magic number: {magic:04x}, expected: 0xA5E0")
        header['magic_number'] = f"0x{magic:04X}"

        header['frames'] = struct.unpack('<H', f.read(2))[0]
        header['width'] = struct.unpack('<H', f.read(2))[0]
        header['height'] = struct.unpack('<H', f.read(2))[0]

        depth = struct.unpack('<H', f.read(2))[0]
        header['color_depth'] = ColorDepth(depth).name

        flags = struct.unpack('<I', f.read(4))[0]
        header['layer_opacity_valid'] = bool(flags & 1)

        header['speed'] = struct.unpack('<H', f.read(2))[0]

        f.read(8)  # Skip set be 0 fields

        header['transparent_index'] = struct.unpack('<B', f.read(1))[0]

        f.read(3)  # Skip ignore bytes

        colors = struct.unpack('<H', f.read(2))[0]
        header['colors'] = 256 if colors == 0 else colors

        header['pixel_width'] = struct.unpack('<B', f.read(1))[0]
        header['pixel_height'] = struct.unpack('<B', f.read(1))[0]

        header['grid_x'] = struct.unpack('<h', f.read(2))[0]
        header['grid_y'] = struct.unpack('<h', f.read(2))[0]
        header['grid_width'] = struct.unpack('<H', f.read(2))[0]
        header['grid_height'] = struct.unpack('<H', f.read(2))[0]

        # Skip remaining header bytes
        f.read(84)

        return header, f
    except:
        f.close()
        raise

