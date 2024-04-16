import numpy as np
import json
import os
import rawpy
from PIL import Image
from queue import PriorityQueue

class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    pq = PriorityQueue()
    for value in frequencies:
        pq.put(HuffmanNode(value, frequencies[value]))
    
    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        pq.put(merged)
    
    return pq.get()

def generate_codes(node, prefix="", code_map={}):
    if node is not None:
        if node.value is not None:
            code_map[node.value] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map

class HuffmanCompression:
    def __init__(self, file_path):
        self.file_path = file_path
        self.shape = None
        self.compressed_binary = None
        self.huffman_tree = None
        self.code_map = {}

    def process_input(self):
        if self.file_path.lower().endswith(('.arw', '.nef', '.cr2', '.dng')):
            with rawpy.imread(self.file_path) as raw:
                rgb = raw.postprocess()
            image_data = np.asarray(rgb, dtype=np.uint8)
        else:
            image_data = np.asarray(Image.open(self.file_path), dtype=np.uint8)
        
        self.shape = image_data.shape
        return image_data.flatten()

    def compress(self, image_data):
        freqs = np.bincount(image_data)
        frequencies = {byte: freq for byte, freq in enumerate(freqs) if freq > 0}

        self.huffman_tree = build_huffman_tree(frequencies)
        self.code_map = generate_codes(self.huffman_tree)

        compressed = ''.join(self.code_map[byte] for byte in image_data)
        self.compressed_binary = compressed

    def save_to_json(self, filename):
        data = {
            'code_map': self.code_map,
            'compressed_binary': self.compressed_binary,
            'shape': self.shape,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.compressed_binary = data['compressed_binary']
        self.code_map = {v: k for k, v in data['code_map'].items()}
        self.shape = tuple(data['shape'])

    def decompress(self):
        decompressed_data = []
        buffer = ""
        for bit in self.compressed_binary:
            buffer += bit
            if buffer in self.code_map:
                decompressed_data.append(self.code_map[buffer])
                buffer = ""
        return np.array(decompressed_data, dtype=np.uint8).reshape(self.shape)

def compare_file_sizes(json_file_path, image_file_path):
    json_size = os.path.getsize(json_file_path)
    image_size = os.path.getsize(image_file_path)
    reduction = image_size - json_size
    reduction_percentage = (reduction / image_size) * 100
    print(f"Original Image Size: {image_size} bytes")
    print(f"Compressed (JSON) Size: {json_size} bytes")
    print(f"Reduction: {reduction} bytes")
    print(f"Reduction Percentage: {reduction_percentage:.2f}%")

def main():
    image_file_path = 'assets/IMG_9544.CR3'  # Update this path to your RAW image file
    compressor = HuffmanCompression(image_file_path)
    image_data = compressor.process_input()
    compressor.compress(image_data)
    
    json_file_path = 'compressed_data.json'
    compressor.save_to_json(json_file_path)
    
    decompressor = HuffmanCompression(image_file_path)
    decompressor.load_from_json(json_file_path)
    decompressed_image = decompressor.decompress()

    decompressed_image_pil = Image.fromarray(decompressed_image)
    decompressed_image_pil.save('decompressed_image.png')

    compare_file_sizes(json_file_path, image_file_path)

if __name__ == "__main__":
    main()
