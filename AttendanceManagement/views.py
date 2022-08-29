from ntpath import join
from django.http import HttpResponse
from django.shortcuts import render
import cv2
import time
import os
import face_recognition

encodeList = []

def home(request):
    return render(request,'home.html')


def addImages(request,id):
    MEDIA_ROOT='static'
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    img_path=os.path.join(MEDIA_ROOT,id)
    print(img_path)
    os.mkdir(img_path)
    ct=0
    while True:
        result, image = cam.read()
        key=cv2.waitKey(1)
        cv2.imshow(id, image)
        f_path=os.path.join(img_path,id+"_"+str(ct)+".png")
        print(f_path)
        cv2.imwrite(f_path,image)
        time.sleep(0.5)
        if ct==10:
            cv2.destroyAllWindows()
            break
        ct=ct+1
    return HttpResponse("Getting Your Image")


def trainModel(request):
    images = []
    classNames = []
    
    path_folder=os.path.join('static')
    users=os.listdir(path_folder)

    for user in users:
        user_path=os.path.join(path_folder,user)
        user_images=os.listdir(user_path)
        for cl in user_images:
            curImg = cv2.imread(f'{user_path}/{cl}')
            images.append(curImg)
            classNames.append(user)

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return HttpResponse("Training Model")