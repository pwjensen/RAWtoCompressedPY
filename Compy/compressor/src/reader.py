import rawpy

def read_raw_image(filepath):
    """
    Reads a RAW image file and converts it to an RGB numpy array.

    Parameters:
    - filepath: str, path to the RAW image file.

    Returns:
    - A numpy array representing the RGB image.
    """
    # Load the RAW image file
    with rawpy.imread(filepath) as raw:
        # Process the image to get an RGB image
        rgb = raw.postprocess()

    return rgb


if __name__ == "__main__":
    # Example usage:
    input_filepath = "assets/Nikon-D610-Shotkit-2.NEF"  # Update this path
    #output_filepath = "assets/converted_image.jpg"  # Update this path

    rgb_image = read_raw_image(input_filepath)

    # Creates a list of colors for each pixel
    rgb_colors = [data[2] for data in rgb_image] 

    #save_image(rgb_image, output_filepath)
    #print(f"Saved converted image to {output_filepath}")
