import numpy as np
import os
from PIL import Image
from queue import PriorityQueue
import rawpy

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

    def save_to_binary(self, filename):
        def serialize_tree(node):
            if node is None:
                return ""
            if node.value is not None:
                return "1" + format(node.value, '08b')  # Assuming byte values for simplicity
            return "0" + serialize_tree(node.left) + serialize_tree(node.right)

        serialized_tree = serialize_tree(self.huffman_tree)
        total_length = len(serialized_tree) + len(self.compressed_binary)
        padding_length = 8 - (total_length % 8)
        padding = '0' * padding_length
        full_binary_string = serialized_tree + self.compressed_binary + padding
        byte_array = bytearray(int(full_binary_string[i:i+8], 2) for i in range(0, len(full_binary_string), 8))

        with open(filename, 'wb') as f:
            f.write(byte_array)

    def load_from_binary(self, filename):
        with open(filename, 'rb') as f:
            byte_array = f.read()
        
        binary_string = ''.join(format(byte, '08b') for byte in byte_array)
        
        def reconstruct_tree(binary_tree_string):
            if binary_tree_string[0] == '1':
                value = int(binary_tree_string[1:9], 2)
                return HuffmanNode(value, 0), binary_tree_string[9:]
            else:
                left_node, rest_binary_string = reconstruct_tree(binary_tree_string[1:])
                right_node, final_rest_binary_string = reconstruct_tree(rest_binary_string)
                parent_node = HuffmanNode(None, left_node.freq + right_node.freq)
                parent_node.left = left_node
                parent_node.right = right_node
                return parent_node, final_rest_binary_string
        
        self.huffman_tree, compressed_data_with_padding = reconstruct_tree(binary_string)
        padding_length = 0
        while compressed_data_with_padding.endswith('0'):
            padding_length += 1
            compressed_data_with_padding = compressed_data_with_padding[:-1]
            if padding_length == 8:
                break
        
        self.compressed_binary = compressed_data_with_padding[:-padding_length]

    def decompress(self):
        decompressed_data = []
        buffer = ""
        for bit in self.compressed_binary:
            buffer += bit
            if buffer in self.code_map:
                decompressed_data.append(self.code_map[buffer])
                buffer = ""
        return np.array(decompressed_data, dtype=np.uint8).reshape(self.shape)

def compare_file_sizes(binary_file_path, image_file_path):
    binary_size = os.path.getsize(binary_file_path)
    image_size = os.path.getsize(image_file_path)
    reduction = image_size - binary_size
    reduction_percentage = (reduction / image_size) * 100
    print(f"Original Image Size: {image_size} bytes")
    print(f"Compressed (Binary) Size: {binary_size} bytes")
    print(f"Reduction: {reduction} bytes")
    print(f"Reduction Percentage: {reduction_percentage:.2f}%")

def main():
    image_file_path = 'assets/Nikon-D750-Image-Samples-2.jpg'  # Update this path to your RAW image file
    compressor = HuffmanCompression(image_file_path)
    image_data = compressor.process_input()
    compressor.compress(image_data)
    
    binary_file_path = 'compressed_data.bin'
    compressor.save_to_binary(binary_file_path)
    
    decompressor = HuffmanCompression(image_file_path)
    decompressor.load_from_binary(binary_file_path)
    decompressed_image = decompressor.decompress()

    decompressed_image_pil = Image.fromarray(decompressed_image)
    decompressed_image_pil.save('decompressed_image.png')

    compare_file_sizes(binary_file_path, image_file_path)

if __name__ == "__main__":
    main()
