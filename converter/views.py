import os
import uuid
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger


def safe_delete(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def home(request):
    return render(request, 'home.html')


# ---------------- PDF TO IMAGE ----------------

def pdf_to_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return render(request, 'pdf_to_image.html', {"error": "No file uploaded"})

        if not uploaded_file.name.endswith('.pdf'):
            return render(request, 'pdf_to_image.html', {"error": "Only PDF files allowed"})

        if uploaded_file.size > 10 * 1024 * 1024:
            return render(request, 'pdf_to_image.html', {"error": "File too large (max 10MB)"})

        fs = FileSystemStorage()
        unique_name = f"{uuid.uuid4()}_{uploaded_file.name}"
        saved_name = fs.save(unique_name, uploaded_file)
        file_path = fs.path(saved_name)

        try:
            images = convert_from_path(file_path)
            os.remove(file_path)
        except Exception:
            return render(request, 'pdf_to_image.html', {"error": "Invalid PDF file"})

        image_urls = []

        for i, image in enumerate(images):
            image_filename = f"{uuid.uuid4()}_page_{i}.png"
            image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
            image.save(image_path, 'PNG')
            image_urls.append(settings.MEDIA_URL + image_filename)

        return render(request, 'result.html', {'files': image_urls})

    return render(request, 'pdf_to_image.html')


# ---------------- IMAGE TO PDF ----------------

def image_to_pdf(request):
    if request.method == 'POST':
        uploaded_images = request.FILES.getlist('images')

        if not uploaded_images:
            return render(request, 'image_to_pdf.html', {"error": "No images uploaded"})

        image_list = []

        for file in uploaded_images:
            if not file.content_type.startswith("image"):
                return render(request, 'image_to_pdf.html', {"error": "Invalid file type"})

            if file.size > 5 * 1024 * 1024:
                return render(request, 'image_to_pdf.html', {"error": "Image too large (max 5MB each)"})

            image = Image.open(file).convert("RGB")
            image_list.append(image)

        output_filename = f"{uuid.uuid4()}.pdf"
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

        return render(request, 'result.html', {'files': [settings.MEDIA_URL + output_filename]})

    return render(request, 'image_to_pdf.html')


# ---------------- MERGE PDF ----------------

def merge_pdf(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')

        if not uploaded_files:
            return render(request, 'merge_pdf.html', {"error": "No files uploaded"})

        fs = FileSystemStorage()
        merger = PdfMerger()
        temp_paths = []

        try:
            # Save uploaded files first
            for file in uploaded_files:
                if not file.name.endswith('.pdf'):
                    return render(request, 'merge_pdf.html', {"error": "Only PDF files allowed"})

                unique_name = f"{uuid.uuid4()}_{file.name}"
                saved_name = fs.save(unique_name, file)
                file_path = fs.path(saved_name)
                temp_paths.append(file_path)

            # Merge from file paths (NOT memory)
            for path in temp_paths:
                merger.append(path)

            output_filename = f"{uuid.uuid4()}.pdf"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            merger.write(output_path)
            merger.close()

        finally:
            # Always clean temp files
            for path in temp_paths:
                if os.path.exists(path):
                    os.remove(path)

        return render(request, 'result.html', {
            'files': [settings.MEDIA_URL + output_filename]
        })

    return render(request, 'merge_pdf.html')
