import numpy as np
import json
import os
import rawpy
from PIL import Image
from queue import PriorityQueue
from binary_encoder import BinaryFileHandler 


# -- for testing BinaryFileHandler 

# converts compressed files to bianry for efficient saving 
import pickle

class BinaryFileHandler:
    
    def __init__(self, code_map, shape, compressed_data):
        self.code_map = code_map  # dict that maps pixel values to Huffman codes
        self.shape = shape  # dimensions of the image for reconstruction
        self.compressed_data = compressed_data  # binary string of compressed data
        self.original_file_size = self.get_data_size(data=compressed_data)
        self.compressed_file_size = None  
    
    def __str__(self) -> str:
        if not self.compressed_file_size:
            return "No File Saved"
        
        # encode the data and return the instance variables 
        meta_data = {"Orginal File Size: " : self.original_file_size,
                     "Compressed File Size: " : self.compressed_file_size,
                     "Size Reduction: " : str(100 - self.compressed_file_size // self.original_file_size) + "%"}

        return str(meta_data)
    
    def get_data_size(self, data):
        # Calculate size in bytes for binary data
        if isinstance(data, str):  # Assuming 'data' is a binary string
            return len(data) // 8
        return len(data)


    def save_binary(self, filename):
        # convert the compressed binary string to bytes
        binary_data = int(self.compressed_data, 2).to_bytes((len(self.compressed_data) + 7) // 8, 'big')
        self.compressed_file_size = self.get_data_size(binary_data)  # Update compressed file size

        # serialize metadata including the updated compressed file size
        metadata = {
            'code_map': self.code_map,
            'shape': self.shape,
            'original_file_size': self.original_file_size,
            'compressed_file_size': self.compressed_file_size,
        }
        metadata_serialized = pickle.dumps(metadata)

        # write serialized metadata and binary data to file
        with open(filename, 'wb') as f:
            f.write(metadata_serialized)
            f.write(binary_data) 

    def load_binary(self, filename):
        with open(filename, 'rb') as f:
            metadata_serialized = f.read() # reading in metadata for reconstruction 
            metadata = pickle.loads(metadata_serialized)
            
            # update instance vars from metadata 
            self.code_map = metadata['code_map']
            self.shape = metadata['shape']
            self.original_file_size = metadata['original_file_size']
            self.compressed_file_size = metadata['compressed_file_size']

            # read the image pixel data
            binary_data = f.read()
            # bytes -> bits conversion 
            self.compressed_data = format(int.from_bytes(binary_data, 'big'), '0{}b'.format(len(binary_data)*8))
# --



class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
        self.bfh = None 
    
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

    # -- using binary_encoder to save files in binary -- 
    def save_to_binary(self, filename): 
        data = {
                'code_map': self.code_map,
                'compressed_binary': self.compressed_binary,
                'shape': self.shape,
            }
        bfh = BinaryFileHandler(code_map=self.code_map, shape=self.shape, compressed_data=self.compressed_data)
        bfh.save_binary(filename=filename)
        self.bfh = bfh 

    def load_from_binary(self, filename): 
        self.bfh = BinaryFileHandler({}, None, None)
        self.bfh.load_binary(filename)
        self.compressed_binary = self.bfh.compressed_data
        self.code_map = self.bfh.code_map
        self.shape = self.bfh.shape
    
def main():
    image_file_path = 'assets/Nikon-D600-Shotkit-2.NEF' 
    compressor = HuffmanCompression(image_file_path)
    image_data = compressor.process_input()
    compressor.compress(image_data)
    
    binary_file_path = 'compressed_output.bin'
    compressor.save_to_binary(binary_file_path)
    decompressor = HuffmanCompression(image_file_path)
    decompressor.load_from_binary(binary_file_path)
    decompressed_image = decompressor.decompress()

    decompressed_image_pil = Image.fromarray(decompressed_image)
    decompressed_image_pil.save('decompressed_image.png')

if __name__ == "__main__":
    main()
