import re
import numpy as np
from PIL import Image

import json

class HuffmanCompressor:
    def __init__(self, img_loc):
        self.image = Image.open(img_loc)
        self.flat_img = np.array(self.image, dtype=np.uint8).flatten()
        self.freq = self.count_frequency()
        self.huffman_tree = self.make_huffman_tree()
        print(self.huffman_tree)
        self.huffman_codes = self.make_huffman_codes(node=self.huffman_tree)
        self.compressed_img = self.huffman_encode()


    def count_frequency(self):
        # counting the frequency of each pixel 
        freq = {}
        for value in self.flat_img:
            if value in freq:
                freq[value] += 1
            else:
                freq[value] = 1
        return freq
    
    def combine_nodes(self, nodes):
        # creating internal nodes 
        while len(nodes) > 1:
            nodes.sort(key=lambda x: x[1])
            right = nodes.pop(0)
            left = nodes.pop(0)
            new_node = ([left[0] + right[0], left[1] + right[1]])
            nodes.append(new_node)
        return nodes[0] # returning root 

    def make_huffman_tree(self):
        # building the tree 
        nodes = [(k, v) for k, v in self.freq.items()]
        tree = self.combine_nodes(nodes)
        return tree

    def print_huffman_tree(self, node, prefix=""):
        # printing the tree recursivley 
        if isinstance(node[0], list):
            self.print_huffman_tree(node[0][0], prefix + "0")
            self.print_huffman_tree(node[0][1], prefix + "1")
        else:
            print(node[0], prefix)

    def make_huffman_codes(self, node, code=""):
        if isinstance(node, tuple) and len(node) == 2 and isinstance(node[0], str):
            # leaf node
            self.huffman_codes[node[0]] = code
        elif isinstance(node, tuple) and len(node) == 3:
            # internal node 
            _, l, r = node
            self.make_huffman_codes(l, code + '0')
            self.make_huffman_codes(r, code + '1')
    
    def huffman_encode(self):
        # encoding each pixel based on generated codes 
        compressed = []

        for pixel in self.flat_img:
            pixel_code = self.huffman_codes.get(str(pixel))
            compressed.append(pixel_code)

        cstr = ''.join(compressed)
        return cstr 

    def save_compressed_data(self, file_path, encoded_img=None):
        if not encoded_img:
            encoded_img = self.compressed_img

        with open(file_path, 'w') as file: 
            json.dump({'compresssed:' : encoded_img, 'codes' : self.huffman_codes})

    def load_compressed_data(self, file_path): 
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.huffman_codes = data['codes']

        return data['compresssed_img']

    def decode_image(self, encoded_img):
        cur = ""  
        decoded_pixels = []

        pixel_map = {v : k for k,v in self.huffman_codes.items()}

        # append each bit to a string until this code exists in the mapping
        for bit in encoded_img:
            cur += bit

            if cur in pixel_map:
                decoded_pixels.append(int(pixel_map[cur]))
                cur="" # reset to build next code

        return np.array(decoded_pixels, dtype=np.unit8).reshape(self.image.size[::-1])
    
if __name__ == '__main__':
    compressor = HuffmanCompressor('assets/example.NEF')
    




    
# # Calculate file size before and after compression
# uncompressed_file_size = len(my_string) * 7
# compressed_file_size = len(binary) - 2
# print("Your original file size was", uncompressed_file_size, "bits. The compressed size is:", compressed_file_size)
# print("This is a saving of ", uncompressed_file_size - compressed_file_size, "bits")


# # Write the compressed data to a file
# output = open("compressed.txt", "w+")
# output.write(bitstring)
# output.close()

# # Decoding section for the Huffman encoded data
# print("Decoding.......")
# bitstring = str(binary[2:])
# uncompressed_string = ""
# code = ""
# for digit in bitstring:
#     code += digit
#     pos = 0
#     for letter in letter_binary:
#         if code == letter[1]:
#             uncompressed_string += letter_binary[pos][0]
#             code = ""
#         pos += 1

# # Display the uncompressed data
# print("Your UNCOMPRESSED data is:")
# temp = re.findall(r'\d+', uncompressed_string)
# res = list(map(int, temp))
# res = np.array(res)
# res = res.astype(np.uint8)
# res = np.reshape(res, shape)
# print(res)
# print("Observe the shapes and input and output arrays are matching or not")
# print("Input image dimensions:", shape)
# print("Output image dimensions:", res.shape)
# data = Image.fromarray(res)
# data.save('uncompressed.png')
# # Check if the original and uncompressed data are the same
# if a.all() == res.all():
#     print("Success")