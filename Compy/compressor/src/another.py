import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from skimage.color import rgb2ycbcr, ycbcr2rgb

def load_image(path):
    # Load an image
    return plt.imread(path)

def apply_dct(image):
    return dct(dct(image.T, norm='ortho').T, norm='ortho')

def apply_idct(image):
    return idct(idct(image.T, norm='ortho').T, norm='ortho')

def quantize(image, q):
    return (image / q).round() * q

def compress_image_color(image, q_factor=50):
    # Convert to YCbCr
    ycbcr_img = rgb2ycbcr(image)
    
    # Process each channel
    channels = []
    for i in range(3):
        # Apply DCT
        dct_image = apply_dct(ycbcr_img[:, :, i])
        
        # Adjust the quantization for chrominance components
        q = q_factor if i == 0 else q_factor * 1.5
        
        # Quantization
        quantized = quantize(dct_image, q)
        
        # Inverse DCT
        reconstructed = apply_idct(quantized)
        channels.append(reconstructed)
    
    # Reconstruct the image
    compressed_img = np.stack(channels, axis=-1)
    
    # Convert back to RGB
    compressed_img_rgb = ycbcr2rgb(compressed_img)
    compressed_img_rgb = np.clip(compressed_img_rgb, 0, 255).astype('uint8')
    
    return compressed_img_rgb

# Load your color image
image_path = 'assets/Nikon-D600-Shotkit-2.NEF'
image = load_image(image_path)

# Compress the image
compressed_image = compress_image_color(image, 50)

# Display the results
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(compressed_image)
plt.title('Compressed Image')

plt.show()
