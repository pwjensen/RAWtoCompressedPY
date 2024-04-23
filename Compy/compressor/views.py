from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from django.http import HttpResponse, FileResponse
from .models import RawImage, CompressedImage
from .forms import RawImageUploadForm
from compressor.src.compressor import HuffmanCompressor
import os 
from PIL import Image

# Create your views here.
def upload_image(request):
    if request.method == 'POST':
        form = RawImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()  # save form 
            # perform compression 

            hc = HuffmanCompressor(img_file=new_image.image.path)     

            # saving img data
            compressed_img = CompressedImage.objects.create(
                original=new_image,
                file_size=hc.raw_size,
                compressed_image=hc.compressed_img,
                compressed_size=hc.compressed_size,
                size_reduction=str(hc.reduction),
                file_loc='assets/original/testing',
            )
            compressed_img.save()

            return redirect('compressed_image_detail', pk=compressed_img.pk) 
        else:
            return HttpResponse("[Invalid Image]")
    else:
        form = RawImageUploadForm()
    return render(request, 'compressor/upload_raw_image.html', {'form': form})


def compressed_image_detail(request, pk):
    compressed_image = get_object_or_404(CompressedImage, pk=pk)
    return render(request, 'compressor/compressed.html', {'compressed_image': compressed_image})


def decompress_and_display(request, pk):
    compressed_image = get_object_or_404(CompressedImage, pk=pk)

    compressor = HuffmanCompressor(img_file=None)  
    encoded_img = compressor.load_compressed_img(compressed_image.img_file)

    decompressed_data = compressor.decode_image(encoded_img)

    image = Image.fromarray(decompressed_data)
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "JPEG")
    image_url = 'assets/Compy/originals/microsoft_office_outlook_logo_icon_145721_tkrJbz5.png'
    return render(request, 'decompress.html', {'image_url': image_url})


def save_compressed_data_to_file(data, filename):
    folder = 'media/compressed_data/'
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = base_filename + '_compressed' + file_extension
    full_path = os.path.join(folder, new_filename)

    with open(full_path, 'wb') as file:
        file.write(data)
    
    return full_path