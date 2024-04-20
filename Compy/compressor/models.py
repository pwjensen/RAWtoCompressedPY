from django.db import models

# Create your models here.

class RawImage(models.Model):
    # Store the original image
    image = models.ImageField(upload_to='assets/originals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
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
    binary_image = models.TextField(default=0) # binary of huffman encoded image
    huffman_guide = models.TextField(default=0) # stores the conversion b/w raw val and huffman encoding
    file_size = models.PositiveIntegerField(default=0)  # Stores file size in bytes
    compressed_at = models.DateTimeField(auto_now_add=True)

