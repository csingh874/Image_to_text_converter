from django.shortcuts import render,HttpResponse
from django.contrib import messages
from .models import ImageUpload
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import pytesseract
from PIL import Image
from django.conf import settings
tesseract_path = r"{}\{}".format(settings.BASE_DIR,"tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path
# Create your views here.

def text_converter(image_name):
    fs = FileSystemStorage()
    fs.save(image_name.name, image_name)
    path = r"{}{}".format(settings.MEDIA_ROOT, image_name.name)
    img = cv2.imread(path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Recognize text with tesseract for python

    result_text =  pytesseract.image_to_string(img)
    fs.delete(image_name.name)
    return result_text


def index(request):
    if request.method == "POST":
        image_name = request.FILES["file_selector"]
        str_image_name = image_name.name.lower()
        if image_name:
            if str_image_name.endswith(".jpg") or str_image_name.endswith(".jpeg") or str_image_name.endswith(".png"):
                result = text_converter(image_name)
                response = HttpResponse()
                response['content_type'] = 'text/plain'
                response['Content-Disposition'] = 'attachment; filename=current.txt'
                response.write(result)
                return response
            else:
                messages.error(request,"Wrong File, Please enter correct file with extension 'JPG','JPEG' or 'PNG;'.")
        else:
            messages.error(request,"Please attach the file.")

    return render(request,"home.html")


def display_image(request):
    return render(request,"view_image.html")