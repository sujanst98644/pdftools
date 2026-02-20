from django.shortcuts import render
import os
from django.conf import settings
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger

def home(request):
    return render(request, 'home.html')

def pdf_to_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        images = convert_from_path(file_path)

        image_paths = []

        for i, image in enumerate(images):
            image_name = f"{uploaded_file.name}_page_{i}.png"
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            image.save(image_path, 'PNG')
            image_paths.append(settings.MEDIA_URL + image_name)

        return render(request, 'result.html', {'files': image_paths})

    return render(request, 'pdf_to_image.html')

def image_to_pdf(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')

        image_list = []
        for img in images:
            image = Image.open(img).convert('RGB')
            image_list.append(image)

        output_path = os.path.join(settings.MEDIA_ROOT, 'output.pdf')
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

        return render(request, 'result.html', {'files': [settings.MEDIA_URL + 'output.pdf']})

    return render(request, 'image_to_pdf.html')

def merge_pdf(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        merger = PdfMerger()

        for f in files:
            merger.append(f)

        output_path = os.path.join(settings.MEDIA_ROOT, 'merged.pdf')
        merger.write(output_path)
        merger.close()

        return render(request, 'result.html', {'files': [settings.MEDIA_URL + 'merged.pdf']})

    return render(request, 'merge_pdf.html')
