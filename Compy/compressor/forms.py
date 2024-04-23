from django import forms 
from .models import RawImage, CompressedImage

class RawImageUploadForm(forms.ModelForm):
    # form for user to submit a raw iamge 
    class Meta:
        model = RawImage
        fields = ['image']