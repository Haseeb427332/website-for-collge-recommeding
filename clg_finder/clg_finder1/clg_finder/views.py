from django.http import HttpResponse
from django.contrib import messages
import json
import os
import string
import random
from django.conf import settings
from django.views.generic import ListView
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage #storing uploaded files
import xlrd #excel read
from .models import *
from django.urls import reverse
from django.shortcuts import render,redirect
import re
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
from users.models import *
from . import forms
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

#def filtering_process(request):
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your College suggestor account.'
            message = render_to_string('commons/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_data23.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_data23.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
def validate_username(request):
    #username = request.GET.get('username', None)
    data = {
        'is_taken': request.user.username
    }
    return JsonResponse(data)
def search(request):
    if request.method == 'POST':
        search = request.POST['srch']
        if search:
            match = clg_details.objects.filter(Q(clg_name__icontains=search)|Q(District__icontains=search))
            print(match)
            if match:
                return render(request,'search.html',{'sr':match})
            else:
                return render(request,'search.html',{'sr':False})
    else:
        return HttpResponseRedirect(reverse('index'))
def clg_infoUpdate(request):
    if request.GET.get('temp_index'):  #for Superuser
        temp_index = request.GET.get('temp_index')
        tempObj = temp.objects.get(id = int(temp_index))
        if(tempObj.clg_id != tempObj.Orign_clg_id):
            if clg_details.objects.get(clg_id = tempObj.clg_id):
                return JsonResponse({"already":True})
            else:
                clg_details.objects.all().filter(clg_id = tempObj.Orign_clg_id).update(clg_id = tempObj.clg_id,clg_name = tempObj.clg_name,District = tempObj.District,University = tempObj.University,contact_details = tempObj.contact_details)
                user_data23.objects.all().filter(staff_clg_code = tempObj.Orign_clg_id).update(staff_clg_code = tempObj.clg_id)
                #return JsonResponse({"Updated":True})
        else:
            clg_details.objects.all().filter(clg_id = tempObj.clg_id).update(clg_name = tempObj.clg_name,District = tempObj.District,University = tempObj.University,contact_details = tempObj.contact_details)
        temp.objects.get(id = int(temp_index)).delete()
        data = {
            "updated":True,
            "id": temp_index
        }
        return JsonResponse(data)
    else:                               #for Staff to requesting changes
        js = request.GET.get('json')
        y = json.loads(js)
        obj = temp.objects.create(Orign_clg_id = request.user.staff_clg_code,clg_id = int(y['instu_codeF']),clg_name = y['clg_name'],District = y['dist'],University = y['uni'],contact_details = y['contact'])
        obj.save()
        return JsonResponse({"soon":True})   
class ajax_adminReg(View):
    def get(self,request):
        em = user_data23.objects.filter(email = request.GET['em'])
        ph = int(request.GET['ap'])
        nm = user_data23.objects.all()
        phone = False
        registered = False
        for i in nm:
            if i.Phone_no == ph:
                phone = True
        if em or phone:
            if em and phone:
                
                data = {
                    'em_error': True,
                    'ph_error' : True
                    }
            elif phone:
                
                data = {
                    'ph_error': True
                    }      
            else:
                
                data = {
                    'em_error' : True
                    }
            return JsonResponse(data)
        else:
            def get_random_alphaNumeric_string(stringLength=8):
                lettersAndDigits = string.ascii_letters + string.digits
                return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
            to_email = request.GET.get('em')
            password = get_random_alphaNumeric_string(8)
            #print(password)
            mail_subject = "College suggestor Account Credentials"
            message = "Hi "+str(request.GET.get('fn'))+" Your College account is successfully created.\nYou can login to our website with this credentials\nEmail ID : "+str(to_email)+"\nPassword : "+str(password)
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            user = user_data23.objects.create_user(request.GET.get('fn'), request.GET.get('em'),password,is_staff= 1,Phone_no = request.GET.get('ap'),last_name = request.GET.get('ln'), staff_clg_code = request.GET.get('pwd'))
            user.save()
            data = {
                'registered' : True
            }
            return JsonResponse(data)

def profileUpdate(request):
    u = request.user
    e = user_data23.objects.filter(email = request.GET.get("e"))
    m = user_data23.objects.filter(Phone_no = request.GET.get("p"))
    if e and not user_data23.objects.filter(email = request.GET.get("e"),id = request.user.id):
        data = {
            'erMail': request.GET.get("e"),
            'Eerror': True
        }
        return JsonResponse(data)
    elif m and not user_data23.objects.filter(Phone_no = request.GET.get("p"),id = request.user.id):
        data = {
            'erPhone':request.GET.get("p"),
            'Perror': True
        }
        return JsonResponse(data)
    else:
        obj = user_data23.objects.get(id=u.id)
        obj.email = request.GET.get('e')
        obj.username = request.GET.get('f')
        obj.Phone_no = request.GET.get('p')

        if request.GET.get('userType') == ('admin' or 'staff'):    
            obj.last_name = request.GET.get('l')
            obj.save()
            data = {
                'noError':True
            }
            return JsonResponse(data)

class Auth_ajax_view(View):
    def get(self,request):
        index_id = request.GET.get('id')
        if request.GET.get('changeRequest'):
            tempObj = temp.objects.get(id = index_id)
            origin = clg_details.objects.all().filter(clg_id = tempObj.Orign_clg_id)[0]
            originSerialize = {'clg_id' : origin.clg_id,'clg_name':origin.clg_name,'District':origin.District,'University':origin.University,'contact_details':origin.contact_details}
            tempSerialize = {'clg_id' : tempObj.clg_id ,'clg_name':tempObj.clg_name,'District':tempObj.District,'University':tempObj.University,'rdate':tempObj.rdate,'contact_details':tempObj.contact_details}
            print(originSerialize)
            print(tempSerialize)
            data = {
                'origin' : originSerialize,
                'tempObj' : tempSerialize,
                'temp_index' : index_id
            }
        else:
            Auth_clg = user_data23.objects.raw("SELECT clg_finder_clg_details.clg_id,clg_finder_clg_details.clg_name,clg_finder_clg_details.District,clg_finder_clg_details.University,clg_finder_clg_details.contact_details,users_user_data23.* FROM clg_finder_clg_details INNER JOIN users_user_data23 ON (users_user_data23.staff_clg_code = clg_finder_clg_details.clg_id) WHERE users_user_data23.id = %s ",[index_id])  
            data1 = serializers.serialize('json', Auth_clg)
            cursor = connection.cursor()
            cursor.execute("SELECT clg_finder_clg_details.clg_id,clg_finder_clg_details.clg_name,clg_finder_clg_details.District,clg_finder_clg_details.University,clg_finder_clg_details.contact_details,users_user_data23.* FROM clg_finder_clg_details INNER JOIN users_user_data23 ON (users_user_data23.staff_clg_code = clg_finder_clg_details.clg_id) WHERE users_user_data23.id = "+ index_id )
            rows = cursor.fetchone()
            data = {
                'AC':rows
            }
        return JsonResponse(data)
class ajax_view_delete(View):
    def get(self,request):
        index_id = request.GET.get('id')
        if request.GET.get('Change_req'):
            temp.objects.get(id = index_id).delete()
        else:
            global_del = user_data23.objects.get(id = index_id).delete()
        data = {
            'id':index_id,
            'deleted' : True
        }
        return JsonResponse(data)
class Auth_ajax_view_delete(View):
    def get(self,request):
        index_id = request.GET.get('id')
        if request.GET.get('fav_del'):
            print(request.GET.get('fav_del'))
            print(request.GET.get('id'))
            fav = favourites.objects.get(fav_college_id = index_id,user_id = request.user.id).delete()
            data = {
            'deleted' : True
            }
            return JsonResponse(data)
        else:
            global_del = user_data23.objects.get(id = index_id).delete()
            data = {
                'deleted' : True
            }
            return JsonResponse(data)
class view_info(View):
    #print("view_info")
    def get(self,request):
        imageObj = user_data23.objects.get(id = request.GET.get('id'))
        try:
            string = imageObj.profile_pic.url
        except:
            string = "/static/pro_pic/7/7.png"
            print("catch")
        else:
            print("else")
            string = imageObj.profile_pic.url
        c_id = request.GET.get('id')
        rows = user_data23.objects.all().filter(id = c_id).values()
        print(type(rows[0]))
        print(rows[0])
        data = {
            'info' : rows[0],
            'string':string
        }
        return JsonResponse(data)
def admin_panel(request):
    context = {}
    selfObj = user_data23.objects.get(id = request.user.id)
    Auth_clg = user_data23.objects.raw("SELECT clg_finder_clg_details.clg_id,clg_finder_clg_details.clg_name,clg_finder_clg_details.District,clg_finder_clg_details.University,clg_finder_clg_details.contact_details,users_user_data23.* FROM clg_finder_clg_details INNER JOIN users_user_data23 ON (users_user_data23.staff_clg_code = clg_finder_clg_details.clg_id)")
    obj = user_data23.objects.all().filter(is_staff = False,is_superuser = False )
    context['changes'] = temp.objects.all()
    context['profileInfo'] = selfObj
    context['users'] = obj
    context['Auth_clg'] = Auth_clg
    return render(request,'admin/admin_panel.html',context)
def homepage(request):
    return render(request,'filters1.html')
def hp(request):
    return render(request,'admin/admin_panel.html')
def addTo_fav(request):
    instu_code = request.GET.get("instu_code")
    if not favourites.objects.all().filter(user_id = request.user.id,fav_college_id = instu_code):
        obj = favourites.objects.create(user_id = request.user.id,fav_college_id = instu_code)
        obj.save()
        data = {'checked':True}
    else:
        obj = favourites.objects.get(user_id = request.user.id,fav_college_id = instu_code).delete()
        data = {'checked':False}
    return JsonResponse(data)
def change_password(request):
    if request.method == 'POST':
        print("hello chnge")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("change")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            form = PasswordChangeForm(request.user,request.POST)
            #messages.error(request, 'Please correct the error below.')
            # return render(request, 'change_password.html', {
            #     'form': form
            #     })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
def index(request):
    def pre_info():
        dist = clg_details.objects.values_list('District', flat=True) # flat = true // return single value instead of tuple " " not (" ") 
        stream = cut_off.objects.values_list('Department',flat=True)
        University = clg_details.objects.values_list('University',flat=True)
        pre_defined_order = []
        def unique(list1):   
            list_set = set(list1) # insert the list to the set  
            unique_list = (list(list_set)) # convert the set to the list
            return unique_list
        district = unique(list(dist))
        district.sort()
        stream_list = unique(list(stream))
        University = unique(list(University))
        # print(district)
        for field in fees._meta.fields: # getting list of caste
            pre_defined_order.append(field.name)
        order=pre_defined_order[2:len(pre_defined_order)]#Caste_list
        context = {"dist":district,
                    "stream_list":stream_list,
                    "caste":order,
                    "University" : University,
                    "user":request.user
        #           "fees":fees_cat,
                    }
        return context
    def execute(str1):
        with connection.cursor() as cursor:
            cursor.execute(str1)
            #cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
            rows = cursor.fetchall()
            #print(type(rows))
            list_clg_details = set(rows)
            # print(list_clg_details)
            # print("hii")
            return list_clg_details
    def meta_caste():
        fees_fields = []
        caste = request.POST['caste']
        for field in cut_off._meta.fields: # getting list of cut_off
            fees_fields.append(field.name)
        for i in fees_fields:
            if(request.POST['gender'] == 'male'):
                if(i.find(caste.upper()) >0 and re.findall("^G",i)):
                    #caste checking for general category "gender=male"
                    return i
            else:
                if(i.find(caste.upper()) >0 and re.findall("^L",i)):
                    return i
    if request.method == 'POST':
        if not request.user.username:
            context = pre_info()
            messages.success(request, "Please login first")
            return render(request,'filters1.html',context)
        print("DD",request.POST['district'])
        #FROM clg_finder_clg_details,clg_finder_cut_off,clg_finder_fees WHERE
        flag = 0
        str1 = "SELECT clg_finder_clg_details.clg_id,clg_finder_clg_details.District,clg_finder_clg_details.clg_name,clg_finder_cut_off.Department FROM clg_finder_clg_details INNER JOIN (clg_finder_cut_off INNER JOIN clg_finder_fees ON clg_finder_fees.clg_id_id = clg_finder_cut_off.clg_id) ON clg_finder_clg_details.clg_id = clg_finder_cut_off.clg_id WHERE " 
        if(request.POST['district'] != '' and request.POST['University'] != '' and request.POST['Department'] != ''):
            str1 += "clg_finder_clg_details.District = '"+str(request.POST['district'])+"' and clg_finder_clg_details.University= '"+str(request.POST['University'])+"' and clg_finder_cut_off.Department= '"+str(request.POST['Department'])+"'"
            flag = 1            
        if(flag != 1):
            if(request.POST['district'] != ''):
                flag = 1
                str1 += "clg_finder_clg_details.District = '"+str(request.POST['district'])+"'"
            if(request.POST['University'] != ''):
                if(flag == 1):
                    str1 += "and clg_finder_clg_details.University= '"+str(request.POST['University'])+"' "
                else:
                    flag = 1
                    str1 += "clg_finder_clg_details.University = '"+str(request.POST['University'])+"' "
            if(request.POST['Department'] != ''):
                if(flag == 1):    
                    str1 += "and clg_finder_cut_off.Department= '"+str(request.POST['Department'])+"' "
                else:
                    str1 += "clg_finder_cut_off.Department= '"+str(request.POST['Department'])+"' "
                    flag = 1
        #print(type(request.POST['gender']))
        if(request.POST['caste'] != '' and request.POST['cet'] != '' and request.POST.get('gender',False) != ''):
            if(flag == 1):
                str1 += "and clg_finder_clg_details.clg_id = clg_finder_cut_off.clg_id and clg_finder_cut_off.av <= CET "
                i = meta_caste()
                str1 = str1.replace("av",i)
                str1 = str1.replace("CET",request.POST['cet']) # making raw query as String that satisfies "if" condition
            else:
                flag = 1
                str1  += "clg_finder_clg_details.clg_id = clg_finder_cut_off.clg_id and clg_finder_cut_off.av <= CET "
                i = meta_caste()
                str1 = str1.replace("av",i)
                str1 = str1.replace("CET",request.POST['cet']) # making raw query as String that satisfies "if" condition
        if(request.POST['caste'] != '' and request.POST['fees'] != '5000'):
            if(flag == 1):
                str1 += "and clg_finder_clg_details.clg_id = clg_finder_fees.clg_id_id and clg_finder_fees.CAST <= FEE "
                str1 = str1.replace("CAST",request.POST['caste'])
                str1 = str1.replace("FEE",request.POST['fees'])
                final_result=execute(str1)
            else:
                flag = 1
                str1 += "clg_finder_fees.clg_id_id=clg_finder_cut_off.clg_id and clg_finder_clg_details.clg_id = clg_finder_fees.clg_id_id and clg_finder_fees.CAST <= FEE "
                str1 = str1.replace("CAST",request.POST['caste'])
                str1 = str1.replace("FEE",request.POST['fees'])
                final_result=execute(str1)
        final_result=execute(str1)
        #print("fR== ",final_result)
        print("FSTR ",str1)
        context={
            'final_result':final_result
        }
        
        return render(request,'listcollege1.html',context)
    else:
        context = pre_info()
        return render(request,'filters1.html',context)
#def demo(request):
def authentication(request):
    admin = request.POST["user"]
    pwd = request.POST["password"]
    varify = authentic.objects.filter(username = admin, password = pwd)
    if not varify:
        return render(request,'Admin_login.html',{'invalid':1})
        #messages.success(request, 's2.html')
    else:
        return render(request,'form.html',{'authenticated':1})
#@login_required(login_url="/")
def xl_upload(request,value = 0):
    def file_save(myfile):
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        loc = uploaded_file_url[1:len(uploaded_file_url)] #to remove 1st slash "/"
        return loc
    def file_process(loc1,f1):
        wb = xlrd.open_workbook(loc1)
        sheet = wb.sheet_by_index(0)
        sheet_columns=[]
        pre_defined_order = []
        for i in range(sheet.ncols): #number of columns
            sheet_columns.append(sheet.cell_value(0,i))
        li_sheet_columns = sheet_columns
        if(f1 == 1):
            file_name = "College_Details"
            for field in clg_details._meta.fields:
                pre_defined_order.append(field.name)
            length = len(pre_defined_order)
        elif(f1 == 2):
            file_name = "Cut Off"
            for field in cut_off._meta.fields:
                pre_defined_order.append(field.name)
            pre_defined_order=pre_defined_order[1:len(pre_defined_order)] #to remove 1st bydefault "id" field
        else:
            file_name = "Fees"
            for field in fees._meta.fields:
                pre_defined_order.append(field.name)
            pre_defined_order=pre_defined_order[1:len(pre_defined_order)]
        context= {
            'file_name' : file_name,
            'UnOrdered':li_sheet_columns,
            'preOrdered':pre_defined_order
            }
        for i in range(sheet.ncols): #checking file column order
            if(pre_defined_order[i] != sheet_columns[i].strip()):
                return context
        query=[]
        clean_list = []
        line_no = 0
        if request.user.is_superuser:
            for i in range(1,sheet.nrows): #feeding data in database
                for j in range(sheet.ncols):
                    query.append(sheet.cell_value(i,j))
        else:
            for i in range(1,sheet.nrows): #feeding data in database
                line_no = line_no + 1
                for j in range(sheet.ncols):
                    query.append(sheet.cell_value(i,j))
                    if j == 0:
                        if request.user.staff_clg_code != sheet.cell_value(i,j):
                            context = {}
                            context['err_instu_code'] = int(sheet.cell_value(i,j))
                            context['line_no'] = line_no
                            context['stf'] = True
                            return context
        line_no = 0
        print("query-->length",len(query))
        for s in query:
            if type(s) == str:
                for a in s:
                    if(a.isprintable()) == False:
                        s=s.replace(a,'')
                clean_list.append(s)
            else:
                clean_list.append(s)
                continue
        count = 1
        distic = []
        def trailing():
            if(f1 == 1):
                del clean_list[:5]
                # print("f1")
            elif(f1 == 2):
                del clean_list[:19]
                # print("f2")
            else:
                # print("f3")
                del clean_list[:8]
        regex = re.compile('[^a-z A-Z 1-9]')
        flag = 2
        flagF2 = 1
        if f1 == 1 or f1 == 2:
            for i in range(len(clean_list)):
                if i == flag and f1 == 1:
                    subs = regex.sub('', clean_list[i])
                    clean_list[i] = subs.strip().capitalize()
                    flag = flag+5
                if i == flagF2 and f1 == 2:
                    subs = regex.sub('', clean_list[i])
                    clean_list[i] = subs.strip().capitalize()
                    flagF2 = flagF2+19
        if request.user.is_superuser:
            for i in range(len(clean_list)):
                if(len(clean_list)==0):
                    break
                query = clean_list
                if(f1 == 1):
                    Clg_details=clg_details(clg_id=clean_list[0],clg_name=clean_list[1],District=clean_list[2],University=clean_list[3],contact_details=clean_list[4])
                    Clg_details.save()
                    trailing()
                    query=[]
                elif(f1 == 2):
                    Cut_off = cut_off(clg_id=query[0],Department=query[1],Intake=query[2],GOPENS=query[3],GSCS=query[4],GSTS=query[5],GVJS=query[6],GNT1S=query[7],GNT2S=query[8],GNT3S=query[9],GOBCS=query[10],LOPENS=query[11],LSCS=query[12],LSTS=query[13],LVJS=query[14],LNT1S=query[15],LNT2S=query[16],LNT3S=query[17],LOBCS=query[18])
                    Cut_off.save()
                    trailing()
                    query=[]
                else:
                    Fees = fees(clg_id_id=query[0],open=query[1],obc=query[2],sc=query[3],st=query[4],sbc=query[5],vj=query[6],nt=query[7])
                    Fees.save()
                    trailing()
                    query=[]
        else:
            for i in range(len(clean_list)):
                if(len(clean_list)==0):
                    break
                query = clean_list
                if(f1 == 1):
                    obj = clg_details.objects.all().filter(clg_id = request.user.staff_clg_code).update(clg_name=clean_list[1],District=clean_list[2],University=clean_list[3],contact_details=clean_list[4])
                    trailing()
                    query=[]
                elif(f1 == 2):
                    obj = cut_off.objects.all().filter(clg_id = request.user.staff_clg_code,Department=query[1]).update(Intake=query[2],GOPENS=query[3],GSCS=query[4],GSTS=query[5],GVJS=query[6],GNT1S=query[7],GNT2S=query[8],GNT3S=query[9],GOBCS=query[10],LOPENS=query[11],LSCS=query[12],LSTS=query[13],LVJS=query[14],LNT1S=query[15],LNT2S=query[16],LNT3S=query[17],LOBCS=query[18])
                    trailing()
                    query=[]
                else:
                    obj = fees.objects.all().filter(clg_id_id = request.user.staff_clg_code).update(open=query[1],obc=query[2],sc=query[3],st=query[4],sbc=query[5],vj=query[6],nt=query[7])
                    trailing()
                    query=[]
        return {}
    def initial_process(request):
        myfile = request.FILES['clg_details']
        loc1 = file_save(myfile)
        f1=1
        state = file_process(loc1,f1)
        print("clg details sucess")
        if(state != {}):
            context = state
            if 'stf' in context :
                print("stf")
                context['fa_name'] = "College Details"
                return context
            return context
        myfile = request.FILES['cut_off']
        loc1 = file_save(myfile)
        f1=2
        state = file_process(loc1,f1)
        print("cutt_off sucess")
        if(state != {}):
            context = state
            if 'stf' in context :
                context['fa_name'] = "cutt_off"
                return context
            return context
        myfile = request.FILES['fees']
        loc1 = file_save(myfile)
        f1=3
        state = file_process(loc1,f1)
        print("feess success")
        if(state != {}):
            context = state
            if 'stf' in context :
                context['fa_name'] = "fees"
                return context
            return context
        else:
            return False    
    if request.user.is_superuser and request.method == 'POST' :
        context = initial_process(request)
        if context:
            return render(request,'uploading.html',context)
        else:
            return render(request, 'uploading.html', {'uploaded_file_url': "File uploaded and processed Successfuly"})
    elif request.user.is_staff and request.method == 'POST':
        context = initial_process(request)
        if context:
            return render(request,'uploading.html',context)
        else:
            return render(request, 'uploading.html', {'uploaded_file_url': "File uploaded and processed Successfuly"})
    else:
        return render(request, 'uploading.html')
@login_required
def form_submission(request): 
    #print("hello world")
    clg_name = request.POST["college_name"]
    instu_code = request.POST["instu_code"]
    Region = request.POST["Region"]
    University = request.POST["University"]
    Contact_details = request.POST["contact_details"]
    Courses = request.POST.getlist("chk")
    #Courses = dict(request.POST)["chk"]
    intake = request.POST.getlist("chk_1")
    caste = request.POST.getlist("caste")
    feess = request.POST.getlist("fees")

    while("" in caste):
        caste.remove("")
    
    Clg_details=clg_details(clg_name=clg_name,clg_id=instu_code,Region=Region,University=University,contact_details=Contact_details)
    Clg_details.save()
    
    def trailing():
        del caste[:16]
        del Courses[:1]
        del intake[:1]

    for i in range(len(Courses)):
        Cut_off=cut_off(Department= Courses[0], Intake=intake[0], clg_id_id= instu_code, GOPENS = caste[0],GSCS=caste[1],GSTS=caste[2],GVJS=caste[3],GNT1S=caste[4],GNT2S=caste[5],GNT3S=caste[6],GOBCS=caste[7],LOPENS=caste[8],LSCS=caste[9],LSTS=caste[10],LVJS=caste[11],LNT1S=caste[12],LNT2S=caste[13],LNT3S=caste[14],LOBCS=caste[15])
        Cut_off.save()    
        trailing()

    Fees = fees(clg_id_id = instu_code, open = feess[0], obc = feess[1], sc = feess[2], st = feess[3], sbc = feess[4], vj_nt = feess[5])
    Fees.save()    

    
    return render(request,'form.html/')
def end(request):
    context = {'excceded':False,
    'photo_limit':0}
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
    return render(request,'formDemo.html')
