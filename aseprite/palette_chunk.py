from typing import BinaryIO, Dict, Any, List
from .chunk import Chunk
import struct

class PaletteEntry:
    def __init__(self):
        self.has_name: bool = False
        self.red: int = 0
        self.green: int = 0
        self.blue: int = 0
        self.alpha: int = 255
        self.name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'rgba': [self.red, self.green, self.blue, self.alpha]
        }
        if self.has_name:
            result['name'] = self.name
        return result

class PaletteChunk(Chunk):
    def __init__(self):
        super().__init__()
        self.palette_size: int = 0
        self.first_color: int = 0
        self.last_color: int = 0
        self.entries: List[PaletteEntry] = []

    @classmethod
    def read(cls, f: BinaryIO, chunk_size: int, chunk_type: int) -> 'PaletteChunk':
        chunk = cls()
        chunk.size = chunk_size
        chunk.type = chunk_type

        # Read palette header
        chunk.palette_size = struct.unpack('<I', f.read(4))[0]
        chunk.first_color = struct.unpack('<I', f.read(4))[0]
        chunk.last_color = struct.unpack('<I', f.read(4))[0]
        f.read(8)  # Skip future bytes

        # Read palette entries
        for _ in range(chunk.last_color - chunk.first_color + 1):
            entry = PaletteEntry()
            flags = struct.unpack('<H', f.read(2))[0]
            entry.has_name = bool(flags & 1)

            entry.red = struct.unpack('<B', f.read(1))[0]
            entry.green = struct.unpack('<B', f.read(1))[0]
            entry.blue = struct.unpack('<B', f.read(1))[0]
            entry.alpha = struct.unpack('<B', f.read(1))[0]

            if entry.has_name:
                name_len = struct.unpack('<H', f.read(2))[0]
                entry.name = f.read(name_len).decode('utf-8')

            chunk.entries.append(entry)

        return chunk

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'PALETTE',
            'size': self.size,
            'parsed': True,
            'palette_size': self.palette_size,
            'first_color': self.first_color,
            'last_color': self.last_color,
            'entries': [entry.to_dict() for entry in self.entries]
        }
