#from django.shortcuts import render
import os
import re
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage #storing uploaded files
import xlrd #excel read
import json
from django.contrib.auth.hashers import make_password,check_password
from babel.numbers import format_currency
from random import randint
from django.shortcuts import redirect
from .models import *
from django.db import IntegrityError
import requests
from django.urls import reverse
from django.contrib import messages
from django.forms import ModelForm
# Create your views here.
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import formView

# class formView(TemplateView):
#     template_name = 'demoo.html'


def formDemo(request):
    if request.method == 'POST':
        print("heloo")
        flag = check_password(request.POST['password'],request.user.password)
        if flag == True:
            form = formView(request.POST,flag=0)
        else:
            form = formView(request.POST,flag=1)
        if form.is_valid():
            print("wrong")
            redirect('formDemo')
        else:
            redirect('formDemo')
    else:
        form = formView()
    context = {
        'form':form
    }
    return render(request,'formDemo.html',context)
def u_index(request):
    return render(request,'sign_up.html')
    #return HttpResponse("hello world")
def u_login(request):
    if request.method == 'POST':
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = authenticate(email=email, password=password)
        if user:
            print("heloo")
            login(request,user)
            #redirect('clg_finder:views1')
            return HttpResponseRedirect(reverse('index'))
        else:
            context={}
            context["error"] = "Credentials are not valid"
            return render(request,'user_login.html',context)
                
    return render(request,'user_login.html')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('u_login'))
def edit_profile(request):
    if request.method == 'POST' :
        form = formView()
        # flag = check_password(request.POST['password'],request.user.password)
        # print(flag)
        # if flag == True:
        #     form = formView(request.POST,flag=0)
        # else:
        #     form = formView(request.POST,flag=1)
        # if form.is_valid():
        #     user_obj = request.user
        #     user_obj.username = request.POST["first_name"]
        #     user_obj.last_name = request.POST["last_name"]
        #     user_obj.email = request.POST["email"]
        #     user_obj.Phone_no = request.POST["phone_num"]
        #     user_obj.password = request.POST["password"]
        #     if myfile:
        #         request.user.profile_pic = myfile
        #     request.user.save()
        # #form = formView()
        # # fname = user_data23.objects.values_list('username',flat = True)
        # # lname = user_data23.objects.values_list('last_name',flat = True)
        # # mail = user_data23.objects.values_list('email',flat = True)
        # # Phone_no = user_data23.objects.values_list('Phone_no',flat = True)
        # # password = user_data23.objects.values_list('password',flat = True)
        na = request.user.username+" "+request.user.last_name
        context = {
            'na' : na,
            'fname' : request.user.username,
            'lname' : request.user.last_name,
            'mail' : request.user.email,
            'Phone_no' : request.user.Phone_no,
            'password' : request.user.password,
            'form':form
        }
        # else:
        #     redirect(users/)
        print(na)
        #print(lname)
        return render(request,'demoo.html',context)
    else:
        # fname = user_data23.objects.values_list('username',flat = True)[0]
        # lname = user_data23.objects.values_list('last_name',flat = True)[0]
        # mail = user_data23.objects.values_list('email',flat = True)[0]
        # Phone_no = user_data23.objects.values_list('Phone_no',flat = True)[0]
        # password = user_data23.objects.values_list('password',flat = True)[0]
        # na = fname+" "+lname
        form = formView()
        
        na = request.user.username+" "+request.user.last_name
        context = {
            'na' : na,
            'fname' : request.user.username,
            'lname' : request.user.last_name,
            'mail' : request.user.email,
            'Phone_no' : request.user.Phone_no,
            'password' : request.user.password,
            'form':form
        }
        print(request.user.Phone_no)
        #print(lname)
        return render(request,'demo.html',context)
def edit_pro_process(request):
    na = request.user.username+" "+request.user.last_name
    if request.method == 'POST':
        flag = check_password(request.POST['password'],request.user.password)
        print(flag)
        if flag == True:
            form = formView(request.POST,flag=0)
        else:
            form = formView(request.POST,flag=1)
        if form.is_valid():
            user_obj = request.user
            user_obj.username = request.POST["first_name"]
            user_obj.last_name = request.POST["last_name"]
            user_obj.email = request.POST["email"]
            user_obj.Phone_no = request.POST["phone_num"]
            user_obj.password = request.POST["password"]
            if myfile:
                request.user.profile_pic = myfile
            request.user.save()
            return render(request,'demo.html',context)
        context = {
            'na' : na,
            'fname' : request.user.username,
            'lname' : request.user.last_name,
            'mail' : request.user.email,
            'Phone_no' : request.user.Phone_no,
            'password' : request.user.password,
            'form':form
        }
    return render(request,'demoo.html',context)
def detailpage(request):
    instu_code = request.POST["instu_code"]
    details =set(clg_details.objects.all().values_list().filter(clg_id = instu_code ))
    #shrink_clg_details = clg_details.objects.values_list('clg_id','clg_name').filter(District=request.POST['district'])
    li_list=list(details)
    fee = list(set(fees.objects.all().values_list().filter(clg_id_id = instu_code)[:1]))
    fcut_off = list(set(cut_off.objects.all().values_list().filter(clg_id = instu_code)))
    #print(fcut_off)
    branch = []
    unique = []
    for f in fcut_off:
        if f[2] not in branch:
            branch.append(f[2])
            unique.append(f)
    format1 = []
    poslist = []
    if fee:
        for f in fee[0]:
            add=format_currency(int(float(f)), 'INR', locale='en_IN')
            add = add[:-3]  # to remove decimal values ".00"
            format1.append(add)
        newlist = []
        for i, p in enumerate(format1):
            newlist.append(p)
        poslist.append(newlist)
    try:
        arr = os.listdir("static/img/"+instu_code)
    except:
        string = "/static/img/logo.jpg"
        template_img = "/static/img/flat.jpg"
    else:
    #print(arr)
        r = re.compile("^logo")
        r1 = re.compile("^flat")
        newlist = list(filter(r.match, arr))
        print(newlist)
        template_img_list = list(filter(r1.match, arr))
        if newlist == 0:
            string = "/static/img/logo.jpg"
        else:
            string = "/static/img/"+instu_code+"/"+newlist[0]
        if template_img_list == 0:
            template_img = "/static/img/flat.jpg"
        else:
            template_img = "/static/img/"+instu_code+"/"+template_img_list[0]
        print(template_img)
    context={
        'detail':li_list,
        'fee':poslist,
        'cut_off':unique,
        'instucode': instu_code,
        'string' : string,
        'template_img' : template_img
        }
    return render(request,'dpage.html',context)
def user_data1(request):
    #return HttpResponse("hello world")
    if request.method == 'POST':
        f_name1 = request.POST["first_name"]
        l_name1 = request.POST["last_name"]
        e_mail = request.POST["email"]
        password = request.POST["password"]
        phone_number = request.POST["phone_num"]
        e = user_data23.objects.filter(email = e_mail)
        m = user_data23.objects.filter(Phone_no = phone_number)
        #print(type(e))
        hpass = make_password(password)
        context = {}
        if e and m:
            print("hii")
            context["Eerror"] = "Email is already registered : "+e_mail
            context["Merror"]="Mobile number is already registered : "+phone_number
            #messages.success(request, f"Email is already registered: {e_mail}")
            return render(request,'sign_up.html',context)
        elif e:
            context["Eerror"] : "Email is already registered : "+e_mail
            return render(request,'sign_up.html',context)
        elif m:
            context["Merror"]:"Mobile number is already registered : "+phone_number
            return render(request,'sign_up.html',context)
        else:
            print(phone_number)
            strPhone = "+91"+str(phone_number)
            otp = randint(1000,9999) #random number generator
            otp = 1234
            context = {
                'f' : f_name1,
                'l' : l_name1,
                'e' : e_mail,
                'p' : hpass,
                'o' : otp,
                'Ph' : phone_number
            }
            return render(request,'otp.html',context)
    else:
        f_name1 = request.GET.get('f')
        l_name1 = request.GET.get('l')
        e_mail = request.GET.get('e')
        password = request.GET.get('p')
        phone_number = request.GET.get('Ph')
        print(f_name1)
        print(phone_number)
        U_data = user_data23(username=f_name1,last_name = l_name1,email=e_mail,password=password,Phone_no=phone_number )
        U_data.save()
        return redirect('/')
        #return render(request,'filters1.html')