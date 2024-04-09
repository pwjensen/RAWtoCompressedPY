import numpy as np
import json
import os
from PIL import Image
import heapq  # More efficient priority queue management
from bitarray import bitarray  # For efficient binary data handling

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

class HuffmanCompression:
    def __init__(self, file_path):
        self.file_path = file_path
        self.shape = None
        self.compressed_binary = bitarray()
        self.huffman_tree = None
        self.code_map = {}

    def process_input(self):
        image_data = np.asarray(Image.open(self.file_path), dtype=np.uint8)
        self.shape = image_data.shape
        return image_data.flatten()

    def compress(self, image_data):
        freqs = np.bincount(image_data)
        frequencies = {byte: freq for byte, freq in enumerate(freqs) if freq > 0}
        
        self.huffman_tree = build_huffman_tree(frequencies)
        self.code_map = generate_codes(self.huffman_tree)
        
        for byte in image_data:
            self.compressed_binary.extend(self.code_map[byte])

    def save_to_json(self, filename):
        code_map_str = {k: v for k, v in self.code_map.items()}
        data = {
            'code_map': code_map_str,
            'compressed_binary': self.compressed_binary.to01(),
            'shape': self.shape,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.compressed_binary = bitarray(data['compressed_binary'])
        self.code_map = {v: int(k) for k, v in data['code_map'].items()}
        self.shape = tuple(data['shape'])

    def decompress(self):
        decompressed_data = []
        buffer = bitarray()
        inv_code_map = {v: k for k, v in self.code_map.items()}
        
        for bit in self.compressed_binary:
            buffer.append(bit)
            if buffer.to01() in inv_code_map:
                decompressed_data.append(inv_code_map[buffer.to01()])
                buffer.clear()
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
    image_file_path = 'assets/Nikon-D750-Image-Samples-2.jpg'  # Update this path to your RAW image file
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
