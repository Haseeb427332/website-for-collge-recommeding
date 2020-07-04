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
from django.http import JsonResponse
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
from django.contrib.auth import update_session_auth_hash
from .forms import formView
from django.contrib.auth.forms import PasswordChangeForm

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
    return HttpResponseRedirect(reverse('login'))
def edit_profile(request):
    context={}
    def imgProcess():
        obj = user_data23.objects.get(id = request.user.id)
        if request.FILES.get('pro_pic'):
            print("files")
            obj.profile_pic = request.FILES.get('pro_pic')
            obj.save()
    def tryCatch():
        obj = user_data23.objects.get(id = request.user.id)
        #string = obj.profile_pic.url
        try:
            string = obj.profile_pic.url
        except:
            string = "/static/pro_pic/7/7.png"
            print("catch")
        else:
            print("else")
            string = obj.profile_pic.url
        print(string)
        return string
    if request.method == 'POST' :
        e = user_data23.objects.filter(email = request.POST.get("email"))
        m = user_data23.objects.filter(Phone_no = request.POST.get("phone_num"))
        # if e and m:
        #     imgProcess()
        #     if not user_data23.objects.filter(email = request.POST.get("email"),id = request.user.id):
        #         context["Eerror"] = "Email is already registered : "+request.POST.get("email")
        #     if not user_data23.objects.filter(Phone_no = request.POST.get("phone_num"),id = request.user.id):
        #         context["Merror"]="Mobile number is already registered : "+request.POST.get("phone_num")
        if e and not user_data23.objects.filter(email = request.POST.get("email"),id = request.user.id):
            print("e")
            imgProcess()
            context["Eerror"] = "Email is already registered : "+request.POST.get("email")
            return render(request,'profile_pg.html',context)
        elif m and not user_data23.objects.filter(Phone_no = request.POST.get("phone_num"),id = request.user.id):
            print("p")
            imgProcess()
            context["Merror"]="Mobile number is already registered : "+request.POST.get("phone_num")
            return render(request,'profile_pg.html',context)
        else:
            imgProcess()
            obj = user_data23.objects.get(id = request.user.id)
            obj.username = request.POST.get("first_name")
            obj.last_name = request.POST.get("last_name")
            obj.email = request.POST.get("email")
            obj.Phone_no = request.POST.get("phone_num")
            
            obj.save()
            string = tryCatch()
            na = obj.username+" "+obj.last_name
            fav_clg = clg_details.objects.raw("SELECT clg_finder_clg_details.clg_id, clg_finder_clg_details.clg_name,users_favourites.user_id FROM clg_finder_clg_details INNER JOIN users_favourites ON (clg_finder_clg_details.clg_id = users_favourites.fav_college_id) WHERE users_favourites.user_id = %s",[request.user.id])    
            context['na'] = na
            context['fname'] = obj.username
            context['lname'] = obj.last_name
            context['mail'] = obj.email
            context['Phone_no'] = obj.Phone_no
            context['string'] = string
            context['fav'] = fav_clg
            return render(request,'profile_pg.html',context)
        # obj = request.user
        # string = tryCatch()
        # na = obj.username+" "+obj.last_name
        # fav_clg = clg_details.objects.raw("SELECT clg_finder_clg_details.clg_id, clg_finder_clg_details.clg_name,users_favourites.user_id FROM clg_finder_clg_details INNER JOIN users_favourites ON (clg_finder_clg_details.clg_id = users_favourites.fav_college_id) WHERE users_favourites.user_id = %s",[request.user.id])
        # context['na'] = na
        # context['fname'] = obj.username
        # context['lname'] = obj.last_name
        # context['mail'] = obj.email
        # context['Phone_no'] = obj.Phone_no
        # context['string'] = string
        # context['fav'] = fav_clg
        # return render(request,'profile_pg.html',context)
    else:
        string = tryCatch()
        na = request.user.username+" "+request.user.last_name
        fav_clg = clg_details.objects.raw("SELECT clg_finder_clg_details.clg_id, clg_finder_clg_details.clg_name,users_favourites.user_id FROM clg_finder_clg_details INNER JOIN users_favourites ON (clg_finder_clg_details.clg_id = users_favourites.fav_college_id) WHERE users_favourites.user_id = %s",[request.user.id])
        context = {
            'na' : na,
            'fname' : request.user.username,
            'lname' : request.user.last_name,
            'mail' : request.user.email,
            'Phone_no' :request.user.Phone_no,
            'password' : request.user.password,
            'string':string,
            'fav':fav_clg
        }
        return render(request,'profile_pg.html',context)
def detailpage(request,value = 0):
    context = {'excceded':False,'photo_limit':0}
    def process(arr,fs,flag,Imagelist):
        if flag == 'g':
            limit = len(arr)
            if limit > 22:
                context['excceded'] = True
            else:
                count = 0
                for i in Imagelist:
                    fs.save(i.name, i)
                    count = count + 1
                    limit = limit+1
                    if limit > 22:
                        context['photo_limit'] = count
                        break
        elif flag == 'c':
            p = re.compile(r'.*(?=\.)')
            for i in arr:                       #getting old "flat" image
                get = p.findall(i)
                if get[0] == 'flat':
                    fs.delete(i)
            form = re.sub(r'.*(?=\.)','',str(Imagelist[0]))
            new_name = 'flat'+form
            fs.save(new_name, Imagelist[0])
        else:
            p = re.compile(r'.*(?=\.)')
            for i in arr:                       #getting old "logo" image
                get = p.findall(i)
                if get[0] == 'logo':
                    fs.delete(i)
            form = re.sub(r'.*(?=\.)','',str(Imagelist[0]))
            new_name = 'logo'+form
            fs.save(new_name, Imagelist[0])
    def file_save(Imagelist,flag):
        folder_name = str(request.user.staff_clg_code)
        try:
            path = os.path.join(settings.MYSTATIC_ROOT,folder_name)
            os.mkdir(path)
        except:
            fs = FileSystemStorage(location=path)
            arr = os.listdir("static/img/"+str(request.user.staff_clg_code))
            process(arr,fs,flag,Imagelist)
        else:
            arr = os.listdir("static/img/"+str(request.user.staff_clg_code))
            fs = FileSystemStorage(location=path)
            process(arr,fs,flag,Imagelist)
    if request.GET.get("imgName"):
        print("img")
        folder_name = str(request.user.staff_clg_code)
        path = os.path.join(settings.MYSTATIC_ROOT,folder_name)
        arr = os.listdir("static/img/"+str(request.user.staff_clg_code))
        fs = FileSystemStorage(location=path)
        for i in arr:
            if i == str(request.GET.get("imgName")):
                fs.delete(i)
                return JsonResponse({'deleted':True})
        return JsonResponse({'deleted':False})
    if request.method == 'POST' and request.FILES.get('multi'):
        print("heloo")
        file_save(request.FILES.getlist('multi'),request.POST['flag'])
        if context['excceded']:
            return JsonResponse({'limitExcced':True})
        elif context['photo_limit'] != 0:
            return JsonResponse({'LimituploadCount':context['photo_limit']})
        else:
            return JsonResponse({'success':True})
    if request.method == 'POST' and request.FILES.get('cover'):
        file_save(request.FILES.getlist('cover'),request.POST['flag'])
    if request.method == 'POST' and request.FILES.get('logo'):
        file_save(request.FILES.getlist('logo'),request.POST['flag'])
    #print(type(value))
    if value == 1 and request.user.is_staff:
        instu_code = request.user.staff_clg_code  
    elif value > 1:
        instu_code = value
        value = 0  
    else:
        try:
            request.user.instu_code = request.POST['instu_code']
            request.user.save()
            instu_code = request.user.instu_code
        except:
            instu_code = request.user.instu_code
    # print(request.user.instu_code)
    details =set(clg_details.objects.all().values_list().filter(clg_id = instu_code))
    li_list=list(details)
    fee = list(set(fees.objects.all().values_list().filter(clg_id_id = instu_code)[:1]))
    fcut_off = list(set(cut_off.objects.all().values_list().filter(clg_id = instu_code)))
    branch = []
    unique = []
    for f in fcut_off:
        if f[2] not in branch:
            branch.append(f[2])
            unique.append(f)
    format1 = []
    poslist = []
    gallaryRE = re.compile("^(?!logo|flat)")
    if fee:
        for f in fee[0]:
            add=format_currency(int(float(f)), 'INR', locale='en_IN')
            add = add[:-3]  # to remove decimal values ".00"
            format1.append(add)
        newlist = []
        for i, p in enumerate(format1):
            newlist.append(p)
        poslist.append(newlist)
        print(instu_code)
    try:
        arr = os.listdir("static/img/"+str(instu_code))
    except:
        string = "/static/img/logo.jpg"
        template_img = "/static/img/flat.jpg"
        gallary = False
        Gstring = False
    else:
        r = re.compile("^logo")
        r1 = re.compile("^flat")
        newlist = list(filter(r.match, arr))
        gallary = list(filter(gallaryRE.match,arr))
        template_img_list = list(filter(r1.match, arr))
        if newlist == []:
            string = "/static/img/logo.jpg"
        else:
            string = "/static/img/"+str(instu_code)+"/"+newlist[0]
        if template_img_list == []:
            template_img = "/static/img/flat.jpg"
        else:
            template_img = "/static/img/"+str(instu_code)+"/"+template_img_list[0]
        if not gallary:
            Gstring = False
        else:
            Gstring = "/static/img/"+str(instu_code)+"/"
    
    context={
        'is_staff':value,
        'gallary':gallary,
        'Gstring' : Gstring,
        'fav_checked':favourites.objects.all().filter(user_id = request.user.id,fav_college_id = instu_code),
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
        #hpass = make_password(password)
        context = {}
        if e and m:
            print("hii")
            context["Eerror"] = "Email is already registered : "+e_mail
            context["Merror"]="Mobile number is already registered : "+phone_number
            #messages.success(request, f"Email is already registered: {e_mail}")
            return render(request,'sign_up.html',context)
        elif e:
            print("e")
            context["Eerror"] = "Email is already registered : "+e_mail
            return render(request,'sign_up.html',context)
        elif m:
            print("p")
            context["Merror"]="Mobile number is already registered : "+phone_number
            return render(request,'sign_up.html',context)
        else:
            print(phone_number)
            strPhone = "+91"+str(phone_number)
            #otp = randint(1000,9999) #random number generator
            otp = 1234
            
            context = {
                'f' : f_name1,
                'l' : l_name1,
                'e' : e_mail,
                'p' : password,
                'o' : otp,
                'Ph' : phone_number
            }
            return render(request,'otp.html',context)
    else:
        if request.GET.get('f') == None:
            return render(request,'sign_up.html')
        else:
            f_name1 = request.GET.get('f')
            l_name1 = request.GET.get('l')
            e_mail = request.GET.get('e')
            password = request.GET.get('p')
            phone_number = request.GET.get('Ph')
            obj = user_data23.objects.create_user(
                username = f_name1,
                last_name = l_name1,
                email = e_mail,
                Phone_no = phone_number,
                password = password
            )
            obj.save()
            # U_data = user_data23(username=f_name1,last_name = l_name1,email=e_mail,password=password,Phone_no=phone_number )
            # U_data.save()
            if request.user:
                print("yes")
                logout(request)
                user = authenticate(email=e_mail, password=password)
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                user = authenticate(email=e_mail, password=password)
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
        return redirect('/')
        #return render(request,'filters1.html')