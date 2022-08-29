from django.http import HttpResponse
from django.shortcuts import render
import cv2
import os

def home(request):
    return render(request,'home.html')
def addImages(request,id):
    path='..\..\static'
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    img_path=os.path.join(path,id+".png")
    print(img_path)
    while True:
        result, image = cam.read()
        key=cv2.waitKey(1)
        cv2.imshow(id, image)
        if key==27:
            cv2.imwrite(id+".png", image)
            cv2.destroyAllWindows()
            break
    return HttpResponse("Getting Your Image")