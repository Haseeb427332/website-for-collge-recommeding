from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .models import *
def index(request):
    return render(request,'sam.html')

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

    
    return render(request,'sam.html/')
def end(request):
    return HttpResponse('second page')
