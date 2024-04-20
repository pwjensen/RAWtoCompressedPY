from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from .models import RawImage, CompressedImage

# Create your views here.
def upload_compress_view(request):
    if request.method == 'POST': 
        file = request.FILES['image'] # uploaded file 
        algorithm = request.POST['algorithm'] # selected algorithm to apply 


        original_img = RawImage(image=file)
        original_img.save()

        # handling the file and applying the compression algo
        # ... 
        
        # huffman tree for decoding (the guide)
        # ... 

        # the encoded file 
        # ... 

        # frequency list of values 
        # ...

        # encoded file size 
        # ... 
        
        # calculated file reduction b/w raw and enc
        # ... 

        return HttpResponse("Image uploaded and Processed")

    # user request == 'GET' 
    algorithm_choices = CompressedImage.ALGORITHM_CHOICES
    
    return render(request, 'compressor/upload.html')