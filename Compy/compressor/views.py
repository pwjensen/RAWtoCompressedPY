from django.shortcuts import render

from django.http import HttpResponse
from .models import RawImage, CompressedImage

# Create your views here.
def upload_compress_view(request):
    if request.method == 'POST': 
        file = request.FILES['image'] # uploaded file 
        algorithm = request.POST['algorithm'] # selected algorithm to apply 


        original_img = OriginalImage(image=file)
        original_img.save()

        # handling the file and applying the compression algo
        # ...

        

        return HttpResponse("Image uploaded and processed using " + algorithm + " algorithm.")

    # user request == 'GET' 
    algorithm_choices = CompressedImage.ALGORITHM_CHOICES
    
    return render(request, 'compressor/upload.html', {'algorithm_choices' : algorithm_choices})

