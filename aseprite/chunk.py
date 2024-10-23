import struct
from typing import BinaryIO, Dict, Any
from enum import IntEnum

class ChunkType(IntEnum):
    OLD_PALETTE_1 = 0x0004
    OLD_PALETTE_2 = 0x0011
    LAYER = 0x2004
    CEL = 0x2005
    CEL_EXTRA = 0x2006
    COLOR_PROFILE = 0x2007
    EXTERNAL_FILES = 0x2008
    MASK = 0x2016
    PATH = 0x2017
    TAGS = 0x2018
    PALETTE = 0x2019
    USER_DATA = 0x2020
    SLICE = 0x2022
    TILESET = 0x2023

class Chunk:
    def __init__(self):
        self.size: int = 0
        self.type: ChunkType = None
        self.raw_data: bytes = None

    @classmethod
    def read(cls, f: BinaryIO, chunk_size: int, chunk_type: int) -> 'Chunk':
        """Read chunk data from file. Override in derived classes."""
        chunk = cls()
        chunk.size = chunk_size
        chunk.type = chunk_type
        chunk.raw_data = f.read(chunk_size - 6)  # -6 for size and type already read
        return chunk

    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk data to dictionary. Override in derived classes."""
        return {
            'type': f"0x{self.type:04X}",
            'size': self.size,
            'parsed': False
        }


