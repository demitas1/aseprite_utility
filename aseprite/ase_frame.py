import struct
from typing import List, Dict, Any, BinaryIO
from .chunk import Chunk, ChunkType
from .palette_chunk import PaletteChunk
from .old_palette_chunk1 import OldPaletteChunk1
from .old_palette_chunk2 import OldPaletteChunk2

class AseFrame:
    def __init__(self):
        self.bytes_size: int = 0
        self.magic: int = 0
        self.chunks: int = 0
        self.duration: int = 0
        self.chunk_data: List[Chunk] = []

    @classmethod
    def read(cls, f: BinaryIO) -> 'AseFrame':
        frame = cls()

        # Read frame header
        frame.bytes_size = struct.unpack('<I', f.read(4))[0]
        frame.magic = struct.unpack('<H', f.read(2))[0]
        old_chunks = struct.unpack('<H', f.read(2))[0]
        frame.duration = struct.unpack('<H', f.read(2))[0]
        f.read(2)  # Skip future bytes
        new_chunks = struct.unpack('<I', f.read(4))[0]

        # Get number of chunks
        frame.chunks = new_chunks if new_chunks > 0 else old_chunks

        # Read all chunks in the frame
        for _ in range(frame.chunks):
            chunk_size = struct.unpack('<I', f.read(4))[0]
            chunk_type = struct.unpack('<H', f.read(2))[0]

            # Create appropriate chunk object based on type
            if chunk_type == ChunkType.PALETTE:
                chunk = PaletteChunk.read(f, chunk_size, chunk_type)
            elif chunk_type == ChunkType.OLD_PALETTE_1:
                chunk = OldPaletteChunk1.read(f, chunk_size, chunk_type)
            elif chunk_type == ChunkType.OLD_PALETTE_2:
                chunk = OldPaletteChunk2.read(f, chunk_size, chunk_type)
            else:
                # For unimplemented chunk types, use base Chunk class
                chunk = Chunk.read(f, chunk_size, chunk_type)

            frame.chunk_data.append(chunk)

        return frame

    def to_dict(self) -> Dict[str, Any]:
        return {
            'bytes_size': self.bytes_size,
            'magic': f"0x{self.magic:04X}",
            'chunks_count': self.chunks,
            'duration': self.duration,
            'chunks': [chunk.to_dict() for chunk in self.chunk_data]
        }

