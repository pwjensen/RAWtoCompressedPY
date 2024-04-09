import numpy as np
from PIL import Image
import heapq
from bitarray import bitarray
import rawpy
import os
import pickle

class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(value, freq) for value, freq in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node):
    stack = [(node, "")]
    code_map = {}
    while stack:
        node, code = stack.pop()
        if node is not None:
            if node.value is not None:
                code_map[node.value] = code
            stack.append((node.right, code + "1"))
            stack.append((node.left, code + "0"))
    return code_map

def compress(image_data):
    freqs = np.bincount(image_data)
    frequencies = {byte: freq for byte, freq in enumerate(freqs) if freq > 0}
    huffman_tree = build_huffman_tree(frequencies)
    code_map = generate_codes(huffman_tree)
    compressed_binary = bitarray()
    for byte in image_data:
        compressed_binary.extend(code_map[byte])
    return compressed_binary, code_map, image_data.shape

def decompress(compressed_binary, code_map, shape):
    inv_code_map = {v: k for k, v in code_map.items()}
    buffer = bitarray()
    decompressed_data = []
    for bit in compressed_binary:
        buffer.append(bit)
        if buffer.to01() in inv_code_map:
            decompressed_data.append(inv_code_map[buffer.to01()])
            buffer.clear()
    return np.array(decompressed_data, dtype=np.uint8).reshape(shape)

def process_input(file_path):
    if file_path.lower().endswith(('.arw', '.nef', '.cr2', '.dng')):
        with rawpy.imread(file_path) as raw:
            rgb = raw.postprocess()
        image_data = np.asarray(rgb, dtype=np.uint8)
    else:
        image_data = np.asarray(Image.open(file_path), dtype=np.uint8)
    return image_data.flatten()

def save_compressed_data(compressed_binary, code_map, shape, compressed_path, code_map_path, shape_path):
    with open(compressed_path, 'wb') as f:
        compressed_binary.tofile(f)
    with open(code_map_path, 'wb') as f:
        pickle.dump(code_map, f)
    with open(shape_path, 'wb') as f:
        pickle.dump(shape, f)

def load_compressed_data(compressed_path, code_map_path, shape_path):
    with open(compressed_path, 'rb') as f:
        compressed_binary = bitarray()
        compressed_binary.fromfile(f)
    with open(code_map_path, 'rb') as f:
        code_map = pickle.load(f)
    with open(shape_path, 'rb') as f:
        shape = pickle.load(f)
    return compressed_binary, code_map, shape

def save_image(image_array, file_path):
    image = Image.fromarray(image_array)
    image.save(file_path)

def compare_file_sizes(original_file_path, compressed_file_paths, decompressed_file_path):
    original_size = os.path.getsize(original_file_path)
    compressed_total_size = sum(os.path.getsize(f) for f in compressed_file_paths)
    decompressed_size = os.path.getsize(decompressed_file_path)
    print(f"Original Image Size: {original_size} bytes")
    print(f"Total Compressed Data Size (including code map and shape): {compressed_total_size} bytes")
    print(f"Decompressed Image Size: {decompressed_size} bytes")

def main():
    image_file_path = 'assets/Nikon-D600-Shotkit-2.NEF'
    compressed_path = 'compressed_image.bin'
    code_map_path = 'code_map.bin'
    shape_path = 'shape.bin'
    decompressed_image_path = 'decompressed_image.png'
    
    # Compress
    image_data = process_input(image_file_path)
    compressed_binary, code_map, shape = compress(image_data)
    save_compressed_data(compressed_binary, code_map, shape, compressed_path, code_map_path, shape_path)
    
    # Decompress
    compressed_binary, code_map, shape = load_compressed_data(compressed_path, code_map_path, shape_path)
    decompressed_data = decompress(compressed_binary, code_map, shape)
    save_image(decompressed_data, decompressed_image_path)

    # Compare file sizes
    compare_file_sizes(image_file_path, [compressed_path, code_map_path, shape_path], decompressed_image_path)

if __name__ == "__main__":
    main()
