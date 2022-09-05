from codecs import EncodedFile
from email.mime import image
from ntpath import join
from django.http import HttpResponse
from django.shortcuts import render
import cv2
import time
import os
import numpy as np
import face_recognition
import json


images = []
classNames = []

def home(request):
    return render(request,'home.html')


def addImages(request,id):
    MEDIA_ROOT='static'
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    img_path=os.path.join(MEDIA_ROOT,id)
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
    path_folder=os.path.join('static')
    users=os.listdir(path_folder)
    
    for user in users:
        user_path=os.path.join(path_folder,user)
        user_images=os.listdir(user_path)
        
        for cl in user_images:
            curImg = cv2.imread(f'{user_path}/{cl}')
            images.append(curImg)
            classNames.append(user)
    return HttpResponse("Training Model")
    
def findEncodings(images):
    encodeListUtil = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if len(face_recognition.face_encodings(img))!=0:
            encode = face_recognition.face_encodings(img)[0]    
        encodeListUtil.append(encode)
    return encodeListUtil

def detectFaces(request):
    encodeListKnown=findEncodings(images)
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            print(len(matches))
            print(len(faceDis))
            print(matchIndex)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # markAttendance(name)

        cv2.imshow('Webcam', img)
        key=cv2.waitKey(1)
        if key==27:
            cv2.destroyAllWindows()
            break
    return HttpResponse("Done with Detecting")