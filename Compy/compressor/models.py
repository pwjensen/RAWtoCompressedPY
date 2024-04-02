from django.db import models

# Create your models here.

class RawImage(models.Model):
    # Store the original image
    image = models.ImageField(upload_to='assets/originals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CompressedImage(models.Model):

    # Encoding formats available to the user 
    HUFFMAN = 'Huffman'
    LZ77 = 'LZ77'
    RLE = 'RLE'

    ENCODER_CHOICES = {
        (HUFFMAN, 'Huffman Encoder'),
        (LZ77, 'LZ77 Encoder'),
        (RLE, 'RLE Encoder')

    }

    # Foreign Key to the original image
    original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE, related_name='compressed_images')
    # Store the compressed image
    compressed_image = models.ImageField(upload_to='images/compressed/')
    # Algorithm used for compression
    algorithm = models.CharField(max_length=50, choices=ENCODER_CHOICES)
    # Compression metrics like size reduction, quality metrics, etc.
    size_reduction = models.FloatField()
    compressed_at = models.DateTimeField(auto_now_add=True)