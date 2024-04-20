from django.contrib import admin
from .models import RawImage, CompressedImage


# Register your models here.
admin.site.register(RawImage)
admin.site.register(CompressedImage)

