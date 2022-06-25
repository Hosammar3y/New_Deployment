from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

#import tensorflow
import cv2
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
#import io

#import PIL
#from PIL import Image
from django.http import JsonResponse

#Create your views here.
@csrf_exempt
def index(request):
    if request.method=="POST":
        if request.FILES["image"]:
            image = request.FILES["image"]
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            file_url = fss.path(file)
            results = get_image_result(file_url, "lcancer_detection/Lung-Cancer-Detection.h5")
            return render(request, "lcancer_detection/result.html", {"result": results})

    return render(request, 'lcancer_detection/index.html')







def get_image_result(image_path, model_path):
    img_size=256
    img = cv2.imread(image_path, 0)
    
    cnn = load_model(model_path)
    
    kernel = np.array([[0, -1, 0],
           [-1, 5,-1],
           [0, -1, 0]])
    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    img = cv2.medianBlur(img,5)
    img = cv2.resize(img, (img_size, img_size))
    image = img_to_array(img)
    image = np.expand_dims(image,axis=0)
    result = cnn.predict(image)
    Normal = [[0,0,1]]
    Maligment= [[0,1,0]]
    Begin=[[1,0,0]]

    if(result[0][2]==1):
      preds = JsonResponse({'state':'Not Cancer'})
    elif(result[0][1]==1):
      preds = JsonResponse({'state':'Cancer', 'type':'Malignant case'})
    else:
      preds = JsonResponse({'state':'Cancer', 'type':'Bengin case'})
    return preds

