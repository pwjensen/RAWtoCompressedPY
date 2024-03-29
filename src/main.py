# main.py
import argparse
from src.compressor import compress_image
from src.reader import read_raw_image

def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description="Compress RAW image files.")
    parser.add_argument('filepath', type=str, help='Path to the RAW image file.')
    parser.add_argument('--output', type=str, help='Output path for the compressed image.', default='compressed.jpg')
    # Add more arguments as needed

    args = parser.parse_args()

    # Read the RAW image
    raw_image = read_raw_image(args.filepath)

    # Compress the image4
    compress_image(raw_image, args.output)

    print(f"Compressed image saved to {args.output}")

if __name__ == "__main__":
    main()
