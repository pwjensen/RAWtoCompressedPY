import numpy as np
import os
import rawpy
from PIL import Image
from queue import PriorityQueue
from bitarray import bitarray
import pickle


def get_file_size(filepath):
    """Returns the size of the file in bytes."""
    size = os.path.getsize(filepath)
    return size

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

def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
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
        try:
            if self.file_path.lower().endswith(('.raw', '.arw', '.nef', '.cr2', '.dng', '.rw2', '.png', '.tif')):
                with rawpy.imread(self.file_path) as raw:
                    print("Processing Image...")
                    rgb = raw.postprocess(half_size=True, use_camera_wb=True, output_bps=16)
                image_data = np.asarray(rgb)
            else:
                image = Image.open(self.file_path)
                image_data = np.asarray(image, dtype=np.uint8) if image.mode == 'RGB' else np.asarray(image.convert('RGB'), dtype=np.uint8)

            self.shape = image_data.shape
            print(f"Image Size: {len(image_data.flatten())} bytes")
            return image_data.flatten()

        except Exception as e:
            print(f"Failed to process image {self.file_path}: {str(e)}")
            return None

    def compress(self, image_data):
        if image_data is None:
            print("No image data to compress.")
            return

        # Calculate frequencies
        print("Calculating Frequencies...")
        freqs = np.bincount(image_data)
        frequencies = {byte: freq for byte, freq in enumerate(freqs) if freq > 0}

        # Build Huffman Tree
        self.huffman_tree = build_huffman_tree(frequencies)
        self.code_map = generate_codes(self.huffman_tree)

        # Encode data
        compressed = bitarray()
        
        total_bytes = len(image_data)
        work_done = 1
        last_printed = -1
        for byte in image_data:
            code = self.code_map.get(byte, '')
            compressed.extend(code)

            # printing status 
            if round((work_done / total_bytes) * 100) % 10 == 0:
                current_percentage = round((work_done / total_bytes) * 100)
                if current_percentage != last_printed:
                    print(f"Compressing... {work_done} / {total_bytes} bytes - [{current_percentage}%]",end='\r')
                    last_printed = current_percentage

            work_done+=1
        # Convert bitarray to bytes
        self.compressed_binary = compressed.tobytes()

        

    def decompress(self):
        if not self.compressed_binary or not self.code_map:
            print("Missing compressed data or code map for decompression.")
            return None

        decompressed_data = []
        buffer = bitarray()
        buffer.frombytes(self.compressed_binary)


        current_code = 0
        current_length = 0
        max_code_length = max(len(code) for code in self.code_map.values())
        work_counter = 0


        print("\nStarting Decompression:")
        last_printed = -1 
        work_done=1
        total_bytes = len(buffer) // 8
        for bit in buffer:
            current_code = (current_code << 1) | bit
            current_length += 1

            if current_length > max_code_length:
                current_code &= (1 << max_code_length) - 1  # Mask to max length
                current_length = max_code_length

            if current_code in self.code_map and len(self.code_map[current_code]) == current_length:
                decompressed_data.append(self.code_map[current_code])
                current_code = 0
                current_length = 0

            # printing status 
            if round((work_done / total_bytes) * 100) % 5 == 0:
                current_percentage = round((work_done / total_bytes) * 100)
                if current_percentage != last_printed:
                    print(f"Decompressing... {work_done} / {total_bytes} bytes - [{current_percentage}]%",end='\r')
                    last_printed = current_percentage

            work_done+=1
            

        # for debugging 
        print("Decompressed data length:", len(decompressed_data))
        print("Expected shape:", self.shape)

        return np.array(decompressed_data, dtype=np.uint8).reshape(self.shape)


def main():

    image_file_path = r'assets/main.ARW'  
    print(f"Original File Size: {get_file_size(image_file_path)}")
    compressor = HuffmanCompression(image_file_path)
    image_data = compressor.process_input()
    compressor.compress(image_data)

    # Save the compressed data to a binary file
    binary_file_path = 'compressed_output.bin'
    with open(binary_file_path, 'wb') as f:
        pickle.dump((compressor.compressed_binary, compressor.code_map, compressor.shape), f)
        print(f"Original File Size: {get_file_size(image_file_path)}")
        print(f"Compressed File Size: {get_file_size(binary_file_path)}")
    # Load and decompress
    with open(binary_file_path, 'rb') as f:
        compressed_binary, code_map, shape = pickle.load(f)
        compressor.compressed_binary = compressed_binary
        compressor.code_map = code_map
        compressor.shape = shape

    decompressed_data = compressor.decompress()
    if decompressed_data is not None:
        print("Decompression successful")
        # Convert numpy array to image and save (if needed)
        decompressed_image = Image.fromarray(decompressed_data.reshape(compressor.shape))
        decompressed_image.save('decompressed_image.png')
    else:
        print("Decompression failed")

    print("\nResults: ")
    print(f"Original File Size: {HuffmanCompression.get_file_size(image_file_path)}")
    print(f"Compressed File Size: {HuffmanCompression.get_file_size(binary_file_path)}")

if __name__ == "__main__":
    main()
