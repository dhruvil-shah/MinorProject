from base64 import encode
from codecs import EncodedFile
# from curses import window
from email.mime import image
from http.client import HTTP_PORT
from logging.handlers import DatagramHandler
from django.http import JsonResponse
from ntpath import join
from colorama import Cursor
from cv2 import RETR_CCOMP
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.views.decorators.cache import cache_control
from record.models import Record
from record.models import CourseStudent
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group

from .forms import CreateUserForm
import cv2
import time
import os
import numpy as np
import face_recognition
import json
from numpy import asarray, roll,save,load


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
        if request.user.is_staff:
            return redirect('home')
        else:
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                if request.user.is_staff:
                    return redirect('home')
                else:
                    return redirect('dashboard')
            else:
                messages.info(request,'Username or Password is Incorrect')

        context={}
        return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home')
        else:
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                if request.user.is_staff:
                    return redirect('home')
                else:
                    return redirect('dashboard')
            else:
                messages.info(request,'Username or Password is Incorrect')

        context={}
        return render(request,'login.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_staff:
        return redirect('home')
    else:
        roll_no=request.user
        print(roll_no)
        courses=getCourses(request,roll_no)
        a1=getAttendance(request,courses.course_1,roll_no,1)
        a2=getAttendance(request,courses.course_2,roll_no,2)
        a3=getAttendance(request,courses.course_d2,roll_no,3)
        a4=getAttendance(request,courses.course_o2,roll_no,4)
        a5=getAttendance(request,courses.course_d1,roll_no,5)
        a6=getAttendance(request,courses.course_o1,roll_no,6)
        lst=[a1,a2,a3,a4,a5,a6]
        context={"data":lst}
        print(lst)
        return render(request,'dashboard.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        return render(request,'home.html')
    else:
        return redirect('dashboard')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
@login_required(login_url='login')
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
@login_required(login_url='login')
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
    encodedListKnown=findEncodings(images)
    data = asarray(encodedListKnown)
    print(data)
    # save('Utils/trainValues.npy', data)
    path="Utils/trainValues"
    with open('{}.npy'.format(path), 'wb+') as f:
        np.save(f, data)
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
        encodeListUtil.append(encode)
    return encodeListUtil

def detectFaces(request,course):
    detectedRoll=set()
    allRoll=set()
    absentRoll=set()
    data=CourseStudent.objects.all()
    for dt in data.iterator():
        if dt.course_1==course or dt.course_2==course or dt.course_d1==course or dt.course_d2==course or dt.course_o1==course or dt.course_o2==course:
            allRoll.add(dt.roll_no)
    
    # file = open("Utils/trainValues.txt", "r")
    # content = file.read()
    # content=np.array(content)
    # print(content[0][0])
    data = load('Utils/trainValues.npy')
    encodeListKnown=data
    # encodeListKnown.append(data)
    # file.close()
    cap = cv2.VideoCapture(0)
    address='https://192.168.1.139:8080/video'
    cap.open(address)
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
            # print(matchIndex)
            # print(len(matches))
            
            if matches[matchIndex]:
                roll = classNames[matchIndex].upper()
                detectedRoll.add(roll)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, roll, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        key=cv2.waitKey(1)
        if key==27:
            cv2.destroyAllWindows()
            absentRoll=allRoll.difference(detectedRoll)
            for roll in detectedRoll:
                rec=Record(roll_no=roll,course=course,time="9-11",present=True)
                rec.save() 
            for roll in absentRoll:
                rec=Record(roll_no=roll,course=course,time="9-11",present=False)
                rec.save()   
            break
    return HttpResponse("Done with Detecting")

def showRecord(request):
    return HttpResponse("Record Shown")

def addSample(request):
    # cs=CourseStudent(roll_no="19BCE161",course_1="2CS701",course_2="2CS702",course_d1="2CSDE01",course_d2="2CSDE02",course_o1="2MEOE01",course_o2="2ICOE02")
    # cs.save()
    return HttpResponse("Done")

def getAttendance(request,course_id,roll_no,sr):
    
    no_present=Record.objects.filter(course=course_id,roll_no=roll_no,present=True)
    no_absent=Record.objects.filter(course=course_id,roll_no=roll_no,present=False)
    percentage=100
    if (len(no_absent)+len(no_present))!=0:
        percentage=(len(no_present)/((len(no_absent)+len(no_present))))*100
    return {"serial_no":sr,"course_id":course_id,'present':len(no_present),'absent':len(no_absent),"percentage":percentage}

def getCourses(request,roll_no):
    course=CourseStudent.objects.get(roll_no=roll_no)
    return course

def courseOption(request):
    context={}
    return render(request,'options.html',context)


