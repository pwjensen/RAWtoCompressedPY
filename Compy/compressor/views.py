from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from django.http import HttpResponse
from .models import RawImage, CompressedImage
from .forms import RawImageUploadForm
from compressor.src.compressor import HuffmanCompressor

# Create your views here.
def upload_image(request):
    if request.method == 'POST':
        form = RawImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()  # save form 
            # perform compression 

            hc = HuffmanCompressor(img_file=new_image.image)     

            # saving img data
            compressed_img = CompressedImage.objects.create(
                original=new_image,
                file_size=hc.raw_size,
                compressed_image=hc.compressed_img,
                size_reduction=str(hc.reduction).format('.2f')
            )
            compressed_img.save()

            return redirect('compressed_image_detail', pk=compressed_img.pk) # 
        else:
            return HttpResponse("[Invalid Image]")
    else:
        form = RawImageUploadForm()
    return render(request, 'compressor/upload_raw_image.html', {'form': form})


def compressed_image_detail(request, pk):
    compressed_image = get_object_or_404(CompressedImage, pk=pk)
    return render(request, 'compressor/compressed.html', {'compressed_image': compressed_image})