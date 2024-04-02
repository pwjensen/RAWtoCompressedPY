import numpy as np
from collections import Counter
import heapq
import json

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(frequencies):
    priority_queue = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0] if priority_queue else None

def generate_codes(node, prefix="", code={}):
    if node is not None:
        if node.char is not None:
            code[node.char] = prefix
        generate_codes(node.left, prefix + "0", code)
        generate_codes(node.right, prefix + "1", code)
    return code

def encode(data, codes):
    return ''.join(codes[char] for char in data)

def compress_image(rgb_array):
    """
    Compresses an RGB image using Huffman coding.
    
    Args:
    - rgb_array: A numpy array of the image in RGB format.

    Returns:
    - A tuple of the encoded image data, the Huffman tree used for encoding, and the original image size.
    """
    # Flatten the RGB data and convert to a sequence of values
    flattened = rgb_array.flatten()
    
    # Original image size
    original_size = rgb_array.shape

    # Calculate frequency of each value
    frequency = Counter(flattened)

    # Build Huffman Tree
    root = build_tree(frequency)

    # Generate Huffman Codes
    codes = generate_codes(root)

    # Encode the image
    encoded_image = encode(flattened, codes)

    # Return encoded data, the tree (for decompression), and original image size
    return encoded_image, root, original_size

def serialize_tree(node):
    if node is None:
        return ""
    if node.char is not None:
        return f"1{chr(node.char)}"
    return f"0{serialize_tree(node.left)}{serialize_tree(node.right)}"

def save_compression(output_path, encoded, tree, original_size):
    serialized_tree = serialize_tree(tree)
    encoded_bytes = int(encoded, 2).to_bytes((len(encoded) + 7) // 8, 'big')
    with open(output_path, 'w') as f:
        json.dump({
            'tree': serialized_tree,
            'encoded': encoded_bytes.hex(),
            'length': len(encoded),
            'original_size': original_size
        }, f)

# Placeholder for the decompression function
def decompress_image(input_path):
    # This function would include loading the compressed data,
    # reconstructing the Huffman tree, and decoding the image.
    pass

# Example usage, assuming you have an RGB numpy array `rgb_array`
if __name__ == "__main__":
    # Example RGB array generation or loading to be replaced with actual image data
    rgb_array = np.random.randint(256, size=(100, 100, 3), dtype=np.uint8)
    
    encoded, tree, original_size = compress_image(rgb_array)
    save_compression("compressed_image.json", encoded, tree, original_size)
    print("Compression completed and saved.")
