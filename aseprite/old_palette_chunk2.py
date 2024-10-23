from typing import BinaryIO, Dict, Any, List
from .chunk import Chunk
import struct

class OldPaletteChunk2(Chunk):
    def __init__(self):
        super().__init__()
        self.num_packets: int = 0
        self.colors: List[Dict[str, int]] = []

    @classmethod
    def read(cls, f: BinaryIO, chunk_size: int, chunk_type: int) -> 'OldPaletteChunk2':
        chunk = cls()
        chunk.size = chunk_size
        chunk.type = chunk_type

        chunk.num_packets = struct.unpack('<H', f.read(2))[0]
        color_index = 0

        for _ in range(chunk.num_packets):
            entries_to_skip = struct.unpack('<B', f.read(1))[0]
            color_index += entries_to_skip

            num_colors = struct.unpack('<B', f.read(1))[0]
            if num_colors == 0:
                num_colors = 256

            for _ in range(num_colors):
                # Old palette format uses 6-bit values (0-63)
                r = struct.unpack('<B', f.read(1))[0] * 255 // 63
                g = struct.unpack('<B', f.read(1))[0] * 255 // 63
                b = struct.unpack('<B', f.read(1))[0] * 255 // 63
                chunk.colors.append({
                    'index': color_index,
                    'rgb': [r, g, b]
                })
                color_index += 1

        return chunk

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'OLD_PALETTE_2',
            'size': self.size,
            'parsed': True,
            'num_packets': self.num_packets,
            'colors': self.colors
        }
