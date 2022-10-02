from base64 import encode
from codecs import EncodedFile
from email.mime import image
from ntpath import join
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.views.decorators.cache import cache_control

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
import cv2
import time
import os
import numpy as np
import face_recognition
import json
from numpy import asarray,save,load


images = []
classNames = []

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was Created for ' + user)
                return redirect('login')

        context={'form':form}
        return render(request,'register.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is Incorrect')

        context={}
        return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is Incorrect')

        context={}
        return render(request,'login.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
@login_required(login_url='login')
def home(request):
    return render(request,'home.html')

def addImages(request,id):
    MEDIA_ROOT='static/dataset'
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
        if ct==2:
            cv2.destroyAllWindows()
            break
        ct=ct+1
    return HttpResponse("Getting Your Image")

def trainModel(request):
    path_folder=os.path.join('static/dataset')
    users=os.listdir(path_folder)
    
    for user in users:
        user_path=os.path.join(path_folder,user)
        user_images=os.listdir(user_path)
        
        for cl in user_images:
            curImg = cv2.imread(f'{user_path}/{cl}')
            images.append(curImg)
            classNames.append(user)
    encodedListKnown=[]
    encodedListKnown.append(findEncodings(images))
    data = asarray(encodedListKnown)
    save('Utils/trainValues.npy', data)
    # file = open("Utils/trainValues.txt", "w+")
    # content = str(encodedListKnown)
    # file.write(content)
    # file.close()
    return HttpResponse("Training Model")
    
def findEncodings(images):
    encodeListUtil = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=[]
        if len(face_recognition.face_encodings(img))!=0:
            encode = face_recognition.face_encodings(img)[0]    
        encodeListUtil=encode
    return encodeListUtil
 
def detectFaces(request):
    # file = open("Utils/trainValues.txt", "r")
    # content = file.read()
    # content=np.array(content)
    # print(content[0][0])
    data = load('Utils/trainValues.npy')
    print(data)
    encodeListKnown=data
    # encodeListKnown.append(data)
    # file.close()
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
            print(matchIndex)
            print(len(matches))
            
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