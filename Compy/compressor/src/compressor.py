import re
import numpy as np
from PIL import Image
import heapq
from collections import namedtuple
import json

class HuffmanCompressor:
    def __init__(self, img_loc):
        # defining a node object
        self.Node = namedtuple('node', ['freq', 'pixels', 'left', 'right'])

        self.image = Image.open(img_loc)
        print("loaded image...")
        self.flat_img = np.array(self.image, dtype=np.uint8).flatten()
        print("flattened image...")
        self.freq = self.count_frequency()
        print("counted frequencies...")
        self.huffman_tree = self.make_huffman_tree()
        print("created huffman tree...")
        self.huffman_codes = {}
        self.make_huffman_codes(self.huffman_tree)
        print("generated huffman codes...")
        #self.print_huffman_tree(self.huffman_tree)
        self.compressed_img = self.huffman_encode()
        print("\nImage Compression Successful!")

    def count_frequency(self):
        freq = np.zeros(256, dtype=np.int32)
        for value in self.flat_img:
            freq[value] += 1
        return freq

    def combine_nodes(self, nodes):
        heapq.heapify(nodes)
        
        while len(nodes) > 1:
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)
            merged_freq = left.freq + right.freq
            merged_pixels = left.pixels + right.pixels
            new_node = self.Node(merged_freq, merged_pixels, left, right)
            heapq.heappush(nodes, new_node)
        return nodes[0]

    def make_huffman_tree(self):
        nodes = [self.Node(freq, str(i), None, None) for i, freq in enumerate(self.freq) if freq > 0]
        return self.combine_nodes(nodes)

    def print_huffman_tree(self, node, prefix=""):
        if node.left is not None and node.right is not None:
            self.print_huffman_tree(node.left, prefix + "0")
            self.print_huffman_tree(node.right, prefix + "1")
        else:
            print(f"Pixel: {node.pixels}, Code: {prefix}")

    def make_huffman_codes(self, node, code=""):
        if node.left is None and node.right is None:
            self.huffman_codes[node.pixels] = code
        else:
            self.make_huffman_codes(node.left, code + '0')
            self.make_huffman_codes(node.right, code + '1')

    def huffman_encode(self):
        compressed = [self.huffman_codes[str(pixel)] for pixel in self.flat_img]
        return ''.join(compressed)
    
    def save_compressed_img(self, file_path): 
        if self.compressed_img:
            with open(file_path, 'w+') as file:
                print(f"Saving Compressed Image to {file_path}")
                json.dump({'compressed' : self.compressed_img, 'codes' : self.huffman_codes}, file)

    def load_compressed_img(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        self.huffman_codes = data['codes']
        return data['compressed']
    
    def decode_image(self, encoded_img):
        cur = ""
        decoded_pixels = []
        pixel_map = {v: k for k, v in self.huffman_codes.items()}
        for bit in encoded_img:
            cur += bit
            if cur in pixel_map:
                decoded_pixels.append(int(pixel_map[cur]))
                cur = ""  # reset to build next code
        return np.array(decoded_pixels, dtype=np.uint8).reshape(self.image.size[::-1])

# test with default image 
if __name__ == '__main__':
    compressor = HuffmanCompressor('assets/example.NEF')

