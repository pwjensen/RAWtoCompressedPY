import re
import numpy as np
from PIL import Image

# Start of the program
print("Huffman Compression Program")
print("=================================================================")

while True:
    try:
        # Get the filename from user
        file = input("Enter the filename:")
        # Load the image, convert it to a numpy array, and ensure type is uint8
        my_string = np.asarray(Image.open(file), np.uint8)
        break  # Exit loop if file is successfully opened
    except IOError:
        print("File not found or unable to read file. Please enter a valid filename.")
# Save the shape of the array
shape = my_string.shape
    # Copy the array to another variable for comparison later
a = my_string
# Display the loaded image data
print ("Entered string is:", my_string)
# Convert array to string to create frequency distribution
my_string = str(my_string.tolist())

# Initialize lists for frequency analysis
letters = []
only_letters = []

# Count frequency of each character in the string
for letter in my_string:
    if letter not in letters:
        frequency = my_string.count(letter)
        letters.append(frequency)
        letters.append(letter)
        only_letters.append(letter)

# Create initial nodes list for the Huffman tree
nodes = []
while len(letters) > 0:
    nodes.append(letters[0:2])
    letters = letters[2:]
nodes.sort()

# Start building the Huffman tree
huffman_tree = []
huffman_tree.append(nodes)

# Function to combine nodes in the Huffman tree
def combine_nodes(nodes):
    pos = 0
    newnode = []
    if len(nodes) > 1:
        nodes.sort()
        nodes[pos].append("1")
        nodes[pos+1].append("0")
        combined_node1 = (nodes[pos][0] + nodes[pos+1][0])
        combined_node2 = (nodes[pos][1] + nodes[pos+1][1])
        newnode.append(combined_node1)
        newnode.append(combined_node2)
        newnodes = [newnode] + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        combine_nodes(nodes)
    return huffman_tree

# Generate the full Huffman tree
newnodes = combine_nodes(nodes)

# Sort and print the Huffman tree
huffman_tree.sort(reverse=True)
print("Huffman tree with merged pathways:")

# Eliminate duplicate nodes in the Huffman tree
checklist = []
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)

# Display levels of the Huffman tree
count = 0
for level in huffman_tree:
    print("Level", count, ":", level)
    count += 1
print()

# Create binary codes for each character
letter_binary = []
if len(only_letters) == 1:
    lettercode = [only_letters[0], "0"]
    letter_binary.append(lettercode * len(my_string))
else:
    for letter in only_letters:
        code = ""
        for node in checklist:
            if len(node) > 2 and letter in node[1]:
                code += node[2]
        lettercode = [letter, code]
        letter_binary.append(lettercode)

# Print binary codes for each character
print("Binary code generated:")
for letter in letter_binary:
    print(letter[0], letter[1])

# Encode the string into a binary representation
bitstring = ""
for character in my_string:
    for item in letter_binary:
        if character in item:
            bitstring += item[1]
binary = "0b" + bitstring
print("Your message as binary is:")

# Calculate file size before and after compression
uncompressed_file_size = len(my_string) * 7
compressed_file_size = len(binary) - 2
print("Your original file size was", uncompressed_file_size, "bits. The compressed size is:", compressed_file_size)
print("This is a saving of ", uncompressed_file_size - compressed_file_size, "bits")

# Write the compressed data to a file
output = open("compressed.txt", "w+")
output.write(bitstring)
output.close()

# Decoding section for the Huffman encoded data
print("Decoding.......")
bitstring = str(binary[2:])
uncompressed_string = ""
code = ""
for digit in bitstring:
    code += digit
    pos = 0
    for letter in letter_binary:
        if code == letter[1]:
            uncompressed_string += letter_binary[pos][0]
            code = ""
        pos += 1

# Display the uncompressed data
print("Your UNCOMPRESSED data is:")
temp = re.findall(r'\d+', uncompressed_string)
res = list(map(int, temp))
res = np.array(res)
res = res.astype(np.uint8)
res = np.reshape(res, shape)
print(res)
print("Observe the shapes and input and output arrays are matching or not")
print("Input image dimensions:", shape)
print("Output image dimensions:", res.shape)
data = Image.fromarray(res)
data.save('uncompressed.png')
# Check if the original and uncompressed data are the same
if a.all() == res.all():
    print("Success")