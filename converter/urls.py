from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pdf-to-image/', views.pdf_to_image, name='pdf_to_image'),
    path('image-to-pdf/', views.image_to_pdf, name='image_to_pdf'),
    path('merge-pdf/', views.merge_pdf, name='merge_pdf'),
]
