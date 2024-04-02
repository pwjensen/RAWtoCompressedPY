from reader import read_raw_image

def run_length_encode(image):
    """Encode a flattened image array using Run-Length Encoding (RLE).

    Args:
        image (list or numpy array): The flattened image data.

    Returns:
        list of tuples: The RLE encoded image, as a list of (value, count) tuples.
    """
    if not image:
        return []

    encoded = []
    prev_pixel = image[0]
    count = 1

    for pixel in image[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoded.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    encoded.append((prev_pixel, count))

    return encoded

# Example usage
if __name__ == "__main__":
    
    input_filepath = "assets/Nikon-D610-Shotkit-2.NEF"
    # Creating a simple example image array
    rgb_image = read_raw_image(input_filepath)
    
    # Encoding the image
    encoded_image = run_length_encode(rgb_image)
    
    print("Encoded image:", encoded_image)
