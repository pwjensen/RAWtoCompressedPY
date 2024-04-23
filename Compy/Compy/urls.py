"""
URL configuration for Compy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include 
from compressor.views import upload_image, compressed_image_detail, decompress_and_display

urlpatterns = [
    path("admin/", admin.site.urls),

    path('upload_raw_image/', upload_image, name='upload_raw'),
    path('compressed/<int:pk>/', compressed_image_detail, name='compressed_image_detail'),
    path('decompress/<int:pk>/', decompress_and_display, name='decompress_display_image'),

]
