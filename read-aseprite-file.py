import argparse
import json
from aseprite.read_header import read_header, ColorDepth
from aseprite.ase_frame import AseFrame

def read_aseprite_file(filepath):
    """Read complete Aseprite file structure."""
    try:
        header, f = read_header(filepath)
        frames = []

        # Read all frames if they exist
        if header['frames'] > 0:
            for i in range(header['frames']):
                frame = AseFrame.read(f)
                frames.append(frame)

        return header, frames
    finally:
        f.close()

def print_file_info(header, frames):
    """Print formatted file information."""
    # Print header
    print("=== Header Information ===")
    print(json.dumps(header, indent=2))

    # Print frame summaries
    if frames:
        print("\n=== Frame Information ===")
        for i, frame in enumerate(frames):
            print(f"\nFrame {i + 1}:")
            print(json.dumps(frame.to_dict(), indent=2))

def main():
    parser = argparse.ArgumentParser(description='Read Aseprite (.ase/.aseprite) file structure')
    parser.add_argument('filepath', help='Path to .ase/.aseprite file')
    args = parser.parse_args()

    try:
        header, frames = read_aseprite_file(args.filepath)
        print_file_info(header, frames)
    except FileNotFoundError:
        print(f"Error: File '{args.filepath}' not found")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
