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

=======
    file_size = models.PositiveIntegerField(default=0)  # Stores file size in bytes

    # when an image is saved this automatically populates its file_size 
    def save(self, *args, **kwargs): 
        self.file_size = self.image.file.size 
        super(RawImage, self).save(*args, **kwargs)

class CompressedImage(models.Model):
    # Foreign Key to the original image
    original = models.ForeignKey(RawImage, on_delete=models.CASCADE, related_name='compressed_images')
    # Store the compressed image
    compressed_image = models.ImageField(upload_to='images/compressed/')
    # Algorithm used for compression
    algorithm = models.CharField(max_length=50, choices=ENCODER_CHOICES)
    # Compression metrics like size reduction, quality metrics, etc.
    size_reduction = models.FloatField()
    compressed_at = models.DateTimeField(auto_now_add=True)
=======
    binary_image = models.TextField(default=0) # binary of huffman encoded image
    huffman_guide = models.TextField(default=0) # stores the conversion b/w raw val and huffman encoding
    file_size = models.PositiveIntegerField(default=0)  # Stores file size in bytes
    compressed_at = models.DateTimeField(auto_now_add=True)
