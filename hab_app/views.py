from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.files.uploadedfile import SimpleUploadedFile
from hab_app.models import *
from datetime import *
from django.apps import apps
from hab_app.forms import *

from student_portal.models import *
from student_portal.forms import *

from django.views.decorators.cache import cache_page

from .resources import *
from tablib import Dataset
# Create your views here

def home(request):

    request.session['hostel_view'] = "a1x"

    flag=0
    for i in AllHostelMetaData.objects.all():
        temp = i.hostelViewPermission
        view_model = apps.get_model(app_label='hab_app', model_name=temp)
        if view_model.objects.filter(webmail=request.session['username']).exists():
            flag=1
            request.session['hostel_view'] = i.hostelName
            break
    if request.session['username'] == "chr_hab":

        hostels = AllHostelMetaData.objects.all()
        return render(request,'hab_app/chrView.html')
    elif AllHostelMetaData.objects.filter(hostelCTid = request.session['username']).exists():
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        return render(request,'hab_app/caretakerView.html',{'ROtable':ROtable})
    elif ChrViewAccess.objects.filter(webmail = request.session['username']).exists():
        return render(request,'hab_app/chrView.html')
    elif flag==1 :
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact=request.session['hostel_view'])
        return render(request,'hab_app/caretakerView.html',{'ROtable':ROtable})
    elif request.session['server']=="202.141.80.12" :
        return render(request,'hab_app/generalView.html')
    else :
        if OccupantDetails.objects.filter(webmail = request.session['username']).exists():
            return render(request,'student_portal/home.html')
        else:
            if request.method == 'GET':
                return render(request,'hab_app/addReqdetails.html')
            if request.method == 'POST':
                if OccupantDetails.objects.filter(idNo = request.POST.get('OccupantId')).exists():
                    student = OccupantDetails.objects.get(idNo = request.POST.get('OccupantId'))
                    student.webmail = request.session['username']
                    student.save()
                    return render(request,'student_portal/home.html')
                else:
                    return HttpResponse("Details not found!!!Contact Caretaker")


def login_page(request):
    return render(request,'hab_app/login.html',{})

@login_required
def logout1(request):
    logout(request)
    return redirect('hab_app:login_page')


def showDetails(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

    else:
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
    if request.method == 'GET':
        parameter = request.GET.get('param')
        details = OccupantDetails.objects.get(idNo = parameter)
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        roDetails = mymodel.objects.get(occupantId__iexact = parameter)
        return render(request,'hab_app/showDetails.html',{'ROtable':ROtable,'details':details,'roDetails':roDetails})

def showDetails2(request):
    if request.method == 'GET':
        parameter = request.GET.get('param')
        pobj = OccupantDetails.models.get(idNo=parameter)
        details = OccupantDetails.objects.get(idNo = parameter)
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        roDetails = mymodel.objects.get(occupantId__iexact = parameter)
        return render(request,'hab_app/showDetails2.html',{'details':details,'roDetails':roDetails})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                request.session['username'] = username
                request.session['password'] = password
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("account not active")
        else:
            return HttpResponse("Invalid Login Credentials")

    else:
        return render(request,'hab_app/login.html')


def vacate(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

    else:
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])

    temp = ROtable.hostelRoomOccupant
    parameter = request.GET.get('param')
    mymodel = apps.get_model(app_label='hab_app', model_name=temp)
    now = datetime.now()
    start = now - timedelta(days=365)
    end = now + timedelta(days=5)
    tobeVacatedShortly = mymodel.objects.filter(toRoomStay__range=(start.date(),end.date()))
    tobeVacatedAll = mymodel.objects.all()
    for i in tobeVacatedShortly:
        if OccupantDetails.objects.filter(idNo__iexact = i.occupantId).exists():
            temp1 = OccupantDetails.objects.get(idNo__iexact = i.occupantId)
            i.name = temp1.name
            i.contact = temp1.mobNo
    for i in tobeVacatedAll:
        if OccupantDetails.objects.filter(idNo__iexact = i.occupantId).exists():
            temp1 = OccupantDetails.objects.get(idNo__iexact = i.occupantId)
            i.name = temp1.name
            i.contact = temp1.mobNo
    if parameter =="1":
        return render(request,'hab_app/vacate.html',{'ROtable':ROtable,'tobeVacated':tobeVacatedShortly})
    else:
        return render(request,'hab_app/vacate.html',{'ROtable':ROtable,'tobeVacated':tobeVacatedAll})

def editRODetails(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

    else:
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])

    temp = ROtable.hostelRoomOccupant
    parameter = request.GET.get('param')
    mymodel = apps.get_model(app_label='hab_app', model_name=temp)
    if request.method == 'GET':
        occupant_id = request.GET.get('param')
        RO_data = mymodel.objects.get(occupantId = occupant_id)
        ROedit_form  = HostelRoomOccupantRelationForm(instance=RO_data)
        return render(request,'hab_app/editRODetails.html',{'ROtable':ROtable,'ROedit_form':ROedit_form})
    if request.method == 'POST':
        form = HostelRoomOccupantRelationForm(request.POST)
        log = mymodel.objects.get(occupantId=request.POST.get('occupantId')).delete()
        if form.is_valid():
            occupantId = form.cleaned_data['occupantId']
            occupant = form.save(commit=False)
            p = mymodel(occupantId = occupantId)
            p.hostelName = occupant.hostelName
            p.roomNo = occupant.roomNo
            p.messStatus = occupant.messStatus
            # p.toMess = occupant.toMess
            # p.fromMess = occupant.fromMess
            p.toRoomStay = occupant.toRoomStay
            p.fromRoomStay = occupant.fromRoomStay
            p.comment = occupant.comment
            p.save()
            return redirect('home')
        else:
            return HttpResponse("Form Invalid")
def editOccupantDetails(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

    else:
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])

    if request.method == 'GET':
        occupant_id = request.GET.get('param')
        occupant_data = OccupantDetails.objects.get(idNo = occupant_id)
        occupantedit_form  = OccupantDetailsEditForm(instance=occupant_data)
        return render(request,'hab_app/editOccupantDetails.html',{'ROtable':ROtable,'occupantedit_form':occupantedit_form})
    if request.method == 'POST':
        instance = get_object_or_404(OccupantDetails, idNo=request.POST.get('idNo'))
        form = OccupantDetailsEditForm(request.POST,request.FILES,instance=instance)
        # log_delete = OccupantDetails.objects.get(idNo=request.POST.get('idNo')).delete()
        if form.is_valid():
            form.save()
            return redirect('hab_app:existingOccupants')
        else:
            return HttpResponse("Form Invalid")


def allot(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = request.session['hostel_view'])
        tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = request.session['hostel_view'],isApprovedChr="Approved")

    else:
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = ROtable.hostelName)
        tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = ROtable.hostelName,isApprovedChr="Approved")
    return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted,'tobeAlloted2':tobeAlloted2})


def chrAllot(request):

    if request.session['username'] == "chr_hab":
        hostels = AllHostelMetaData.objects.all()
        if request.method == 'POST':
            form = UpcomingOccupantForm(data=request.POST)
            if form.is_valid():
                occupant = form.save()
                occupant.save()
                form = UpcomingOccupantForm()
                return render(request,'hab_app/addOccupant.html',{'form':form})
            else:
                print(form.errors)

        else:
            form = UpcomingOccupantForm()
            return render(request,'hab_app/addOccupant.html',{'form':form})
    else:
        return HttpResponse("You are not Authorized to access this page!!!")

def addDetails(request):

    if request.session['hostel_view']!="a1x":

        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        if request.method == 'POST':

            form1 = HostelRoomOccupantRelationForm(data=request.POST)
            form2 = OccupantDetailsForm(request.POST, request.FILES)
            if form1.is_valid():
                print("tes")
                occupantId = form1.cleaned_data['occupantId']
                occupant = form1.save(commit=False)
                p = mymodel(occupantId = occupantId)
                p.hostelName = ROtable.hostelName
                p.roomNo = occupant.roomNo
                p.messStatus = occupant.messStatus
                # p.toMess = occupant.toMess
                # p.fromMess = occupant.fromMess
                p.toRoomStay = occupant.toRoomStay
                p.fromRoomStay = occupant.fromRoomStay
                p.comment = occupant.comment
                p.save()


                if form2.is_valid():
                    instance = form2.save(commit=False)
                    instance.idNo = occupantId
                    instance.save()
                else:
                    print(form2.errors)
            else:
                print(form1.errors)
            log = UpcomingOccupant.objects.get(occupantId = occupantId).delete()
            tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = ROtable.hostelName)
            return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted})

        if request.method == 'GET':

            occupantId = request.GET.get('param')
            tobeAlloted = UpcomingOccupant.objects.get(occupantId = occupantId)
            initialData1 = {'occupantId': tobeAlloted.occupantId,'hostelName': tobeAlloted.hostelName,'roomNo': tobeAlloted.roomNo,'fromRoomStay': tobeAlloted.fromStay,'toRoomStay': tobeAlloted.toStay}
            initialData2 = {'name':tobeAlloted.occupantName,'idType':tobeAlloted.idType}
            form1 = HostelRoomOccupantRelationForm(initial = initialData1)
            form2 = OccupantDetailsForm(initial = initialData2)
            return render(request,'hab_app/temp.html',{'form1':form1,'form2':form2})

def ct_add_occupant(request):

    if request.session['hostel_view']=="a1x":

        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        if request.method == 'POST':

            form1 = HostelRoomOccupantRelationForm(data=request.POST)
            form2 = OccupantDetailsForm(request.POST, request.FILES)
            if form1.is_valid():
                print("tes")
                occupantId = form1.cleaned_data['occupantId']
                if OccupantDetails.objects.filter(idNo = occupantId).exists():
                    return HttpResponse("Occupant Id Already Exists!!!")
                occupant = form1.save(commit=False)
                p = mymodel(occupantId = occupantId)
                p.hostelName = ROtable.hostelName
                p.roomNo = occupant.roomNo
                p.messStatus = occupant.messStatus
                # p.toMess = occupant.toMess
                # p.fromMess = occupant.fromMess
                p.toRoomStay = occupant.toRoomStay
                p.fromRoomStay = occupant.fromRoomStay
                p.comment = occupant.comment
                p.save()


                if form2.is_valid():
                    instance = form2.save(commit=False)
                    instance.idNo = occupantId
                    instance.save()
                else:
                    print(form2.errors)
            else:
                print(form1.errors)

            return redirect('home')

        if request.method == 'GET':

            form1 = HostelRoomOccupantRelationForm(initial={'hostelName':ROtable.hostelName})
            form2 = OccupantDetailsForm()
            return render(request,'hab_app/ct_add_occupant.html',{'form1':form1,'form2':form2,'ROtable':ROtable})

def addDetails2(request):

    if request.session['hostel_view']!="a1x":

        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        if request.method == 'POST':

            form1 = HostelRoomOccupantRelationForm(data=request.POST)
            form2 = OccupantDetailsForm(request.POST, request.FILES)
            if form1.is_valid():
                print("tes")
                occupantId = form1.cleaned_data['occupantId']
                occupant = form1.save(commit=False)
                p = mymodel(occupantId = occupantId)
                p.hostelName = ROtable.hostelName
                p.roomNo = occupant.roomNo
                p.messStatus = occupant.messStatus
                # p.toMess = occupant.toMess
                # p.fromMess = occupant.fromMess
                p.toRoomStay = occupant.toRoomStay
                p.fromRoomStay = occupant.fromRoomStay
                p.comment = occupant.comment
                p.save()

                if form2.is_valid():
                    instance = form2.save(commit=False)
                    instance.idNo = occupantId
                    instance.save()
                else:
                    print(form2.errors)
            else:
                print(form1.errors)
            log = UpcomingOccupantRequest.objects.get(id_no = occupantId,isApprovedChr="Approved").delete()
            tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = ROtable.hostelName)
            tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = ROtable.hostelName,isApprovedChr="Approved")
            return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted,'tobeAlloted2':tobeAlloted2})

        if request.method == 'GET':

            occupantId = request.GET.get('param')
            tobeAlloted = UpcomingOccupantRequest.objects.get(id_no = occupantId,isApprovedChr="Approved")
            initialData1 = {
                            'occupantId': tobeAlloted.id_no,'hostelName': tobeAlloted.hostelName,
                            'fromRoomStay': tobeAlloted.From_Date,'toRoomStay': tobeAlloted.To_Date,

                        }
            initialData2 = {
                            'name':tobeAlloted.guestname,'idType':tobeAlloted.id_type,
                            'gender':tobeAlloted.Gender,'saORda':tobeAlloted.saORda,
                            'webmail':tobeAlloted.Webmail_id,'altEmail':tobeAlloted.Alternate_email_id,
                            'mobNo':tobeAlloted.Mobile_No,'emgercencyNo':tobeAlloted.Emergency_Mobile_No,
                            'Address':tobeAlloted.Address,'Pincode':tobeAlloted.Pincode,
                            'bankName':tobeAlloted.Bank_Name,'bankAccount':tobeAlloted.Bank_Account_No,
                            'IFSCCode':tobeAlloted.IFSCCode,'accHolderName':tobeAlloted.Account_Holder_Name,
                            'photo':tobeAlloted.photo,'idPhoto':tobeAlloted.idPhoto,
                        }

            form1 = HostelRoomOccupantRelationForm(initial = initialData1)
            form2 = OccupantDetailsForm(initial = initialData2)
            return render(request,'hab_app/temp.html',{'form1':form1,'form2':form2})

def deleteDetails(request):

    if request.method == 'GET':
        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        occupantId = request.GET.get('param')
        occupant = mymodel.objects.get(occupantId__iexact=occupantId)
        p = Log_Table(occupantId = occupantId)
        p.hostelName = ROtable.hostelName
        p.roomNo = occupant.roomNo
        p.messStatus = occupant.messStatus
        # p.toMess = occupant.toMess
        # p.fromMess = occupant.fromMess
        p.toRoomStay = occupant.toRoomStay
        p.fromRoomStay = occupant.fromRoomStay
        p.comment = occupant.comment
        p.save()
        occupant = mymodel.objects.get(occupantId=occupantId).delete()
        now = datetime.now()
        start = now - timedelta(days=365)
        end = now + timedelta(days=5)
        tobeVacated = mymodel.objects.filter(toRoomStay__range=(start.date(),end.date()))
        for i in tobeVacated:
            temp1 = OccupantDetails.objects.get(idNo__iexact = i.occupantId)
            i.name = temp1.name
            i.contact = temp1.mobNo
        return render(request,'hab_app/vacate.html',{'ROtable':ROtable,'tobeVacated':tobeVacated})


def existingOccupants(request):

    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

    else:

        ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
    temp = ROtable.hostelRoomOccupant
    mymodel = apps.get_model(app_label='hab_app', model_name=temp)
    relation = mymodel.objects.all()
    occupants = list()
    relation_list = list()
    for i in relation:
        if OccupantDetails.objects.filter(idNo__iexact=i.occupantId).exists():
            occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
            relation_list.append(i)
    zipped = zip(relation_list,occupants)
    return render(request,'hab_app/existingOccupants.html',{'ROtable':ROtable,'zipped':zipped})


def roomDetails(request):
    if request.method == 'GET':
        index = request.GET.get('param')
        #occupied rooms
        #get the relation table name and room table name

        if request.session['hostel_view']!="a1x":
            ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])

        else:

            ROtable = AllHostelMetaData.objects.get(hostelCTid = request.session['username'])
        relation_table = ROtable.hostelRoomOccupant
        room_table = ROtable.hostelRoom
        # get the model names for query
        relation_model = apps.get_model(app_label='hab_app', model_name=relation_table)
        room_model = apps.get_model(app_label='hab_app', model_name=room_table)
        relation = relation_model.objects.all()
        occupants = list()
        room_list = list()
        for i in relation:
            if datetime.now().date() <= i.toRoomStay and datetime.now().date() >= i.fromRoomStay:
                if OccupantDetails.objects.filter(idNo__iexact=i.occupantId).exists():
                    if room_model.objects.filter(roomNo = i.roomNo).exists():
                        occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
                        room_list.append(room_model.objects.get(roomNo = i.roomNo))

        zipped = zip(room_list,occupants)
        #for empty rooms
        empty_rooms = list()
        all_rooms = room_model.objects.all()
        for i in all_rooms:
            flag = 0
            for j in room_list:
                if i.roomNo == j.roomNo:
                    flag = 1
                    break
            if flag == 0:
                empty_rooms.append(i)
        if index == "1":
            return render(request,'hab_app/occupiedRooms.html',{'ROtable':ROtable,'zipped':zipped})

        elif index == "2":
            #empty rooms
            return render(request,'hab_app/emptyRooms.html',{'ROtable':ROtable,'empty_rooms':empty_rooms})

        else:
            return render(request,'hab_app/totalRooms.html',{'ROtable':ROtable,'zipped':zipped ,'empty_rooms':empty_rooms})



def generalAllot(request):
    if request.method == 'POST':
        form = UpcomingOccupantRequestForm(request.POST , request.FILES)
        if form.is_valid():
            occupant = form.save(commit=False)
            occupant.save()
            obj = User.objects.get(username = request.session['username'])
            initialData = {'Host_Name':obj.first_name,'Host_Webmail_Id':obj.username}
            form1 = UpcomingOccupantRequestForm(initial = initialData)
            return render(request,'hab_app/generalAllot.html',{'form':form1})
        else:
            print(form.errors)
    else:
        obj = User.objects.get(username = request.session['username'])
        initialData = {'Host_Name':obj.first_name,'Host_Webmail_Id':obj.username}
        form = UpcomingOccupantRequestForm(initial = initialData)
        return render(request,"hab_app/generalAllot.html",{'form':form})


def trackApplication(request):
    applicants = UpcomingOccupantRequest.objects.filter(Host_Webmail_Id = request.session['username'])
    return render(request,"hab_app/generalTrack.html",{'applicants':applicants})

# def approveApplication(request):
#     if request.method == 'GET':
#         if request.GET.get('param') :
#             idNo = request.GET.get('param')
#             guest = UpcomingOccupantRequest.objects.get(id_no = idNo)
#             guest.isApprovedFirst = "Approved"
#             guest.save()
#     applicants = UpcomingOccupantRequest.objects.filter(To_be_approved_by__iexact = request.session['username'] , isApprovedFirst = "Pending" )
#     return render(request,"hab_app/approveApplication.html",{'applicants':applicants})
#
#
# def disapproveApplication(request):
#     if request.method == 'GET':
#         if request.GET.get('param') :
#             idNo = request.GET.get('param')
#             guest = UpcomingOccupantRequest.objects.get(id_no = idNo)
#             guest.isApprovedFirst = "Disapproved"
#             guest.save()
#     applicants = UpcomingOccupantRequest.objects.filter(To_be_approved_by__iexact = request.session['username'] , isApprovedFirst = "Pending" )
#     return render(request,"hab_app/approveApplication.html",{'applicants':applicants})

def chrApproveApplication(request):


    hostels = AllHostelMetaData.objects.all()
    if request.method == 'GET':
        if request.GET.get('param') :
            idNo = request.GET.get('param')
            guest = UpcomingOccupantRequest.objects.get(id_no = idNo,isApprovedChr="Pending")
            form =UpcomingOccupantRequestChrForm(instance=guest)
            return render(request,"hab_app/chrApproveEdit.html",{'form':form,'guest':guest})
    if request.method == 'POST':
        form = UpcomingOccupantRequestChrForm(request.POST,request.FILES)
        guest = UpcomingOccupantRequest.objects.get(id_no = request.POST.get('id_no'),isApprovedChr="Pending").delete()
        if form.is_valid():
            upcoming_occupant = form.save(commit=False)
            if 'ap' in request.POST :
                upcoming_occupant.isApprovedChr = "Approved"
                upcoming_occupant.save()
            elif 'dp' in request.POST:
                upcoming_occupant.isApprovedChr = "Disapproved"
                upcoming_occupant.save()
        else:
            print(form.errors)
    applicants = UpcomingOccupantRequest.objects.filter(isApprovedChr = "Pending" )
    return render(request,"hab_app/chrApproveApplication.html",{'applicants':applicants})


# def chrDisapproveApplication(request):
#
#     if request.method == 'GET':
#         if request.GET.get('param') :
#             idNo = request.GET.get('param')
#             # guest = UpcomingOccupantRequest.objects.get(id_no = idNo,isApprovedChr="Pending")
#             # guest.isApprovedChr = "Disapproved"
#             # guest.save()
#
#     applicants = UpcomingOccupantRequest.objects.filter(isApprovedChr = "Pending" )
#     return render(request,"hab_app/chrApproveApplication.html",{'applicants':applicants})

@cache_page(10 * 60)
def chrViewRoom(request):

    if request.method == 'GET':
        if request.GET.get('param') :
            hostel = request.GET.get('param')
            ROtable = AllHostelMetaData.objects.get(hostelName__iexact = hostel)
            relation_table = ROtable.hostelRoomOccupant
            room_table = ROtable.hostelRoom
            # get the model names for query
            relation_model = apps.get_model(app_label='hab_app', model_name=relation_table)
            room_model = apps.get_model(app_label='hab_app', model_name=room_table)
            relation = relation_model.objects.all()
            occupants = list()
            room_list = list()
            for i in relation:
                if datetime.now().date() <= i.toRoomStay and datetime.now().date() >= i.fromRoomStay:
                    if OccupantDetails.objects.filter(idNo__iexact=i.occupantId).exists():
                        if room_model.objects.filter(roomNo = i.roomNo).exists():
                            occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
                            room_list.append(room_model.objects.get(roomNo = i.roomNo))

            zipped = zip(room_list,occupants)
            #for empty rooms
            empty_rooms = list()
            all_rooms = room_model.objects.all()
            for i in all_rooms:
                flag = 0
                for j in room_list:
                    if i.roomNo == j.roomNo:
                        flag = 1
                        break
                if flag == 0:
                    empty_rooms.append(i)
            hostels = AllHostelMetaData.objects.all()
            return render(request,'hab_app/chrViewRoom.html',{'ROtable':ROtable,'zipped':zipped ,'empty_rooms':empty_rooms})

@cache_page(10 * 60)
def chrViewSpecialRooms(request):

    if request.method == 'GET':
        if request.GET.get('param') :
            hostel = request.GET.get('param')
            ROtable = AllHostelMetaData.objects.get(hostelName__iexact = hostel)
            relation_table = ROtable.hostelRoomOccupant
            room_table = ROtable.hostelRoom
            # get the model names for query
            relation_model = apps.get_model(app_label='hab_app', model_name=relation_table)
            room_model = apps.get_model(app_label='hab_app', model_name=room_table)
            relation = relation_model.objects.all()
            occupants = list()
            room_list = list()
            for i in relation:

                if OccupantDetails.objects.filter(idNo__iexact=i.occupantId).exists():
                    if room_model.objects.filter(roomNo = i.roomNo).exists():
                        if room_model.objects.filter(roomNo = i.roomNo,special_category__in=[1,2]).exists():
                            occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
                            room_list.append(room_model.objects.get(roomNo = i.roomNo))

            zipped = zip(room_list,occupants)
            #for empty rooms
            empty_rooms = list()
            all_rooms = room_model.objects.all()
            for i in all_rooms:
                flag = 0
                for j in room_list:
                    if i.roomNo == j.roomNo:
                        flag = 1
                        break
                if flag == 0:
                    if i.special_category != 0:
                        empty_rooms.append(i)
            hostels = AllHostelMetaData.objects.all()
            return render(request,'hab_app/chrViewSpecialRooms.html',{'ROtable':ROtable,'zipped':zipped ,'empty_rooms':empty_rooms})

@cache_page(10 * 60)
def chrHostelSummary(request):

    hostels = AllHostelMetaData.objects.all()
    hostelSummary = list()
    for i in hostels.iterator():
        curr_hostel = list()
        hostel = i.hostelName
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = hostel)
        relation_table = ROtable.hostelRoomOccupant
        room_table = ROtable.hostelRoom
        # get the model names for query
        relation_model = apps.get_model(app_label='hab_app', model_name=relation_table)
        room_model = apps.get_model(app_label='hab_app', model_name=room_table)
        relation = relation_model.objects.all()
        room_list = list()

        for i in relation:
            if datetime.now().date() <= i.toRoomStay and datetime.now().date() >= i.fromRoomStay:
                if room_model.objects.filter(roomNo = i.roomNo).exists():
                    room_list.append(room_model.objects.get(roomNo = i.roomNo))


        #for empty rooms
        # empty_rooms = list()
        all_rooms = room_model.objects.all()
        #total rooms
        curr_hostel.append( room_model.objects.all().count())
        #occupied rooms
        curr_hostel.append(len(room_list))
        abandoned=0
        usable=0
        partial=0
        first=0
        second=0
        third=0
        ground=0
        usable_list=list()

        for i in all_rooms.iterator():
            if i.roomStatus == "Abandoned":
                abandoned= abandoned+1
            if i.roomStatus == "Usable":
                usable=usable+1
                usable_list.append(i)

            if i.roomStatus == "Partially Damaged":
                partial=partial+1

            # flag = 0
            # for j in room_list:
            #     if i.roomNo == j.roomNo:
            #         flag = 1
            #         break
            # if flag == 0:
            #     empty_rooms.append(i)

        for i in usable_list:
            flag=0
            for j in room_list:
                if i.roomNo == j.roomNo:
                    flag=1
                    break
            if flag==0 :
                if str(i.roomOccupancyType) == "Single Occupancy" or str(i.roomOccupancyType) == "Double Occupancy":
                    if i.floorInfo == "First Floor" :
                        first=first+1
                    if i.floorInfo == "Second Floor":
                        second=second+1
                    if i.floorInfo == "Third Floor":
                        third=third+1
                    if i.floorInfo == "Ground Floor":
                        ground=ground+1
        #ready to be alloted
        curr_hostel.append(ground)
        curr_hostel.append(first)
        curr_hostel.append(second)
        curr_hostel.append(third)
        curr_hostel.append(first+second+third+ground)
        curr_hostel.append(abandoned)
        hostelSummary.append(curr_hostel)
    total = [0]*8

    for i in hostelSummary:
        for j in range(8):
            total[j] = total[j] + i[j]
    # return HttpResponse(total)
    zipped_summary = zip(hostelSummary,hostels)
    return render(request,'hab_app/chrHostelSummary.html',{'zipped_summary':zipped_summary,'total':total})



def chrCaretakerView(request):
    if request.method == 'GET':
        request.session['hostel_view'] = request.GET.get('param')
        username = request.session['hostel_view']
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = username)
        return render(request,'hab_app/caretakerView.html',{'ROtable':ROtable})

# chairman uploading csv file for bulk allottment
def chrFreshersBulkAllot(request):
    if request.method == 'GET':
        return render(request,'hab_app/FreshersBulkAllotUpload.html')

    if request.method=="POST":
        csv_file = request.FILES['csv_file']
        #return HttpResponse(csv_file)
        freshers_bulkallot_resource = FreshersBulkAllotResource()
        dataset = Dataset()
        imported_data = dataset.load(csv_file.read().decode('utf-8'))
        print(imported_data)
        result = freshers_bulkallot_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
                freshers_bulkallot_resource.import_data(dataset, dry_run=False)
        return render(request,'hab_app/chrView.html')


#delete room
def chrRoomDelete(request,hostel_name):
    hostelRoomstring = hostel_name+"Room"
    hostelRoomModel = apps.get_model(app_label='hab_app', model_name=hostelRoomstring)
    if request.method == 'GET':
        if request.GET.get('param3'):
            roomNo = request.GET.get('param3')
            hostelRoomModel.objects.filter(roomNo = roomNo).delete()
            roomdetailslist = hostelRoomModel.objects.all()
            return render(request,'hab_app/chrRoomDetailsPage.html',{'roomdetailslist':roomdetailslist,'hostelname':hostel_name})





def chrRoomDetailsEdit(request):
    if request.method == 'GET':
        if request.GET.get('param'):
            hostelname = request.GET.get('param')
            hostelRoomstring = hostelname+"Room"
            hostelRoomModel = apps.get_model(app_label='hab_app', model_name=hostelRoomstring)
            roomdetailslist = hostelRoomModel.objects.all()
            return render(request,'hab_app/chrRoomDetailsPage.html',{'roomdetailslist':roomdetailslist,'hostelname':hostelname})


def chrRoomDetailsEdit2(request,hostel_name):
    hostelRoomstring = hostel_name+"Room"
    hostelRoomModel = apps.get_model(app_label='hab_app', model_name=hostelRoomstring)
    if request.method == 'GET':
        if request.GET.get('param2'):
            roomNo = request.GET.get('param2')
            RoomObject = hostelRoomModel.objects.get(roomNo=roomNo)
            initialData = {

                            'roomNo': RoomObject.roomNo ,   #should not be changed
                            'roomOccupancyType': RoomObject.roomOccupancyType ,
                            'floorInfo' : RoomObject.floorInfo ,
                            'roomStatus': RoomObject.roomStatus ,
                            'roomOccupancyGender' : RoomObject.roomOccupancyGender ,
                            'comments' : RoomObject.comments,

                        }
            form = chrRoomDetailsEditForm(initial = initialData)
            return render(request,'hab_app/RoomEditingForm.html',{'form':form ,})

    if request.method == 'POST':
        form = chrRoomDetailsEditForm(request.POST)
        if form.is_valid():
            if 'upd' in request.POST:
                roomNo = form.cleaned_data.get('roomNo')
                hostel_room = hostelRoomModel.objects.get(roomNo = roomNo)
                hostel_room.roomOccupancyType = form.cleaned_data.get('roomOccupancyType')
                hostel_room.floorInfo = form.cleaned_data.get('floorInfo')
                hostel_room.roomStatus = form.cleaned_data.get('roomStatus')
                hostel_room.roomOccupancyGender = form.cleaned_data.get('roomOccupancyGender')
                hostel_room.comments = form.cleaned_data.get('comments')
                hostel_room.save()

            if 'del' in request.POST:
                roomNo = form.cleaned_data.get('roomNo')
                hostelRoomModel.objects.filter(roomNo = roomNo).delete()


        else:
            print(form.errors)
            return HttpResponse("error")
        roomdetailslist = hostelRoomModel.objects.all()
        return render(request,'hab_app/chrRoomDetailsPage.html',{'roomdetailslist':roomdetailslist,'hostelname':hostel_name})





#add a room
def chrRoomAdd(request,hostel_name):
    if request.method == 'GET':
        form = chrRoomDetailsEditForm(initial = None)
        return render(request,'hab_app/RoomAddForm.html',{'form':form ,})
    if request.method == 'POST':
        form = chrRoomDetailsEditForm(request.POST)
        if form.is_valid():
            hostelRoomstring = hostel_name+"Room"
            hostelRoomModel = apps.get_model(app_label='hab_app', model_name=hostelRoomstring)
            roomNo = form.cleaned_data.get('roomNo')
            if hostelRoomModel.objects.filter(roomNo = roomNo).count() > 0:
                return HttpResponse("Room with same room number already exists")
            else:
                roomOccupancyType = form.cleaned_data.get('roomOccupancyType')
                floorInfo = form.cleaned_data.get('floorInfo')
                roomStatus = form.cleaned_data.get('roomStatus')
                roomOccupancyGender = form.cleaned_data.get('roomOccupancyGender')
                comments = form.cleaned_data.get('comments')
                hostelRoomModel.objects.create(roomNo = roomNo,roomOccupancyType = roomOccupancyType,
                                                floorInfo = floorInfo,roomStatus=roomStatus,
                                                roomOccupancyGender = roomOccupancyGender,
                                                comments = comments)



        else:
            print(form.errors)
            return HttpResponse("error")

        roomdetailslist = hostelRoomModel.objects.all()
        return render(request,'hab_app/chrRoomDetailsPage.html',{'roomdetailslist':roomdetailslist,'hostelname':hostel_name})










def caretakerapproveinfo(request):

    if request.session['hostel_view']!="a1x":
        temp =  AllHostelMetaData.objects.get(hostelName__iexact=request.session['hostel_view'])
    else:

        temp =  AllHostelMetaData.objects.get(hostelCTid=request.session['username'])
    hostelname = temp.hostelName
    hostelROstring = hostelname+"RORelation"
    hostelROModel = apps.get_model(app_label='hab_app', model_name=hostelROstring)
    students_info_update =[]
    students_ro = []
    toapprove_info_list_total = TemporaryDetails.objects.filter(ct_approval="Pending")
    for student in toapprove_info_list_total:
        if hostelROModel.objects.filter(occupantId = student.idNo  ).exists():
            students_info_update.append(student)
            students_ro.append(hostelROModel.objects.get(occupantId = student.idNo  ))
    zipped = zip(students_info_update,students_ro)

    if request.method == 'GET':
        if request.GET.get('param') :
            idNo=request.GET.get('param')
            student1 = TemporaryDetails.objects.get(idNo = idNo,ct_approval="Pending")
            initialData = {
                        'name':student1.name,'idType':student1.idType,
                        'gender':student1.gender,'saORda':student1.saORda,
                        'altEmail':student1.altEmail,'idNo':student1.idNo,
                        'mobNo':student1.mobNo,'emgercencyNo':student1.emgercencyNo,
                        'Address':student1.Address,'Pincode':student1.Pincode,
                        'bankName':student1.bankName,'bankAccount':student1.bankAccount,
                        'IFSCCode':student1.IFSCCode,'accHolderName':student1.accHolderName,
                        'photo':student1.photo,'idPhoto':student1.idPhoto,'webmail':student1.webmail,
                    }
            form = CtApproveStudentEditForm(initial=initialData)
            return render(request,"hab_app/CTapproveEdit.html",{'form':form,'ROtable':temp})



    if request.method == 'POST':

        form =CtApproveStudentEditForm(request.POST , request.FILES)

        log_stud = TemporaryDetails.objects.get(idNo = request.POST.get('idNo'),ct_approval="Pending")
        if form.is_valid():
            # return HttpResponse(request.FILES.get('photo'))
            temporary_data = form.save(commit=False)
            if not temporary_data.photo:
                temporary_data.photo = log_stud.photo
            if not temporary_data.idPhoto:
                temporary_data.idPhoto = log_stud.idPhoto
            log_stud = TemporaryDetails.objects.get(idNo = request.POST.get('idNo'),ct_approval="Pending")
            if 'd' in request.POST:
                log_stud.ct_approval = "Disapproved"
                log_stud.save()
            elif 'a' in request.POST :
                # return HttpResponse(temporary_data.photo)
                print(temporary_data)
                log_stud.ct_approval = "Approved"
                log_stud.save()
                log = OccupantDetails.objects.get(idNo=temporary_data.idNo).delete()
                p = OccupantDetails()
                p.name = temporary_data.name
                #id type - roll no/aadhar no/project id etc
                p.idType =temporary_data.idType
                #rollno/aadhar no etc
                #primary_key removed temp
                p.idNo =temporary_data.idNo
            #vgv
                p.gender =temporary_data.gender
                #specially abled/differently abled
                p.saORda =temporary_data.saORda
                p.webmail =temporary_data.webmail
                p.altEmail = temporary_data.altEmail
                p.mobNo = temporary_data.mobNo
                p.emgercencyNo =temporary_data.emgercencyNo
                p.photo = temporary_data.photo
                p.idPhoto = temporary_data.idPhoto
                p.Address=temporary_data.Address
                p.Pincode=temporary_data.Pincode
                p.bankName = temporary_data.bankName
                p.bankAccount = temporary_data.bankAccount
                p.IFSCCode = temporary_data.IFSCCode
                #account holder name
                p.accHolderName = temporary_data.accHolderName
                p.flag = 1
                p.save()

                students_info_update =[]
                students_ro = []
                toapprove_info_list_total = TemporaryDetails.objects.filter(ct_approval="Pending")
                for student in toapprove_info_list_total:
                    if hostelROModel.objects.filter(occupantId = student.idNo  ).count() == 1:
                        students_info_update.append(student)
                        students_ro.append(hostelROModel.objects.get(occupantId = student.idNo))
                zipped = zip(students_info_update,students_ro)
                return render(request,"hab_app/caretaker_student_info_tobeupdated.html",{'zipped':zipped,'ROtable':temp})
        else:
            print(form.errors)

    return render(request,"hab_app/caretaker_student_info_tobeupdated.html",{'zipped':zipped,'ROtable':temp})
# Mess OPI Related views
#month and year calculations for the display of last month graph
curr_month = datetime.now().month
curr_year = datetime.now().year
m1 = curr_month
y1 = curr_year
m1 = m1 - 1
m1_y1 = ""
if m1 < 1:
    m1 = 12
    y1 = y1 - 1
m11 = m1 -1
y11 = y1
if m11 < 1:
    m11 = 12
    y11 = y11 - 1
m111 = m11 -1
y111 = y11
if m111 < 1:
    m111 = 12
    y111 = y111 - 1


def mess_opi(request):
    permission2=1
    data = Opi_calculated.objects.filter(month=m1,year=y1)
    data1 = Opi_calculated.objects.filter(month=m11,year=y11)
    print(data1)
    # data.append(data1)
    print(data)
    return render(request,'hab_app/mess_opi.html', {'data': data, 'data1': data1,'permission2':permission2})

def opi_calculate(request):
    permission2=1
    feedbacks = MessFeedback.objects.filter(month=m1,year=y1)
    # print(feedbacks)
    hostelss = []
    noh = 0         # number of hostels
    freq_hostelss = []  #hostel wise freq of the feedback
    for fb in feedbacks:
        #   count No. of feedbacks hostelwise
        if fb.hostelName not in hostelss:
            hostelss.append(fb.hostelName)
            noh = noh + 1
            freq_hostelss.append(1)
        else:# print(feedbacks)
            freq_hostelss[hostelss.index(fb.hostelName)] += 1

#   one loop to calculate sum of 5 fields hostelwise and then take their average
    opis = [0] * len(hostelss)
    cleanliness_av = [0] * len(hostelss)
    breakfast_quality_av = [0] * len(hostelss)
    lunch_quality_av = [0] * len(hostelss)
    dinner_quality_av = [0] * len(hostelss)
    catering_av = [0] * len(hostelss)

    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = (fb.cleanliness + fb.qual_b + fb.qual_l + fb.qual_d + fb.catering)/5
        cleanliness_av[hostelss.index(fb.hostelName)] += fb.cleanliness
        breakfast_quality_av[hostelss.index(fb.hostelName)] += fb.qual_b
        lunch_quality_av[hostelss.index(fb.hostelName)] += fb.qual_l
        dinner_quality_av[hostelss.index(fb.hostelName)] += fb.qual_d
        catering_av[hostelss.index(fb.hostelName)] += fb.catering
    print(opis)
    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = opis[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
        cleanliness_av[hostelss.index(fb.hostelName)] = cleanliness_av[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
        breakfast_quality_av[hostelss.index(fb.hostelName)] = breakfast_quality_av[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
        lunch_quality_av[hostelss.index(fb.hostelName)] = lunch_quality_av[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
        dinner_quality_av[hostelss.index(fb.hostelName)] = dinner_quality_av[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
        catering_av[hostelss.index(fb.hostelName)] = catering_av[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
    # Opi_calculated.objects.filter(month=m111,year=y111).delete()
    for i in range(len(opis)):
        if len(Opi_calculated.objects.filter(month=m1,year=y1)) == 0 :
            opi_object = Opi_calculated(hostelName=hostelss[i])
            opi_object.opi_value = opis[i]
            opi_object.numberOfSubscriptions = freq_hostelss[i]
            opi_object.cleanliness_av = cleanliness_av[i]
            opi_object.breakfast_quality_av = breakfast_quality_av[i]
            opi_object.lunch_quality_av = lunch_quality_av[i]
            opi_object.dinner_quality_av = dinner_quality_av[i]
            opi_object.catering_av = catering_av[i]
            opi_object.save()
        else:
            opi_object = Opi_calculated.objects.filter(month=m1,year=y1)[0]
            Opi_calculated.objects.filter(month=m1,year=y1).delete()
            opi_object.hostelName = hostelss[i]
            opi_object.opi_value = opis[i]
            opi_object.numberOfSubscriptions = freq_hostelss[i]
            opi_object.cleanliness_av = cleanliness_av[i]
            opi_object.breakfast_quality_av = breakfast_quality_av[i]
            opi_object.lunch_quality_av = lunch_quality_av[i]
            opi_object.dinner_quality_av = dinner_quality_av[i]
            opi_object.catering_av = catering_av[i]
            opi_object.save()
    print('Opi Calculated')
    return redirect('hab_app:mess_opi')

def mess_automation(request):
    permission2=1
    if request.method == 'GET':
        objects_all  = Automation.objects.all().order_by('-year')
        if request.GET.get('param2'):
                mth_yr = request.GET.get('param2')
                mth = mth_yr.split('_')
                month = int(mth[0])
                year = int(mth[1])
                log = Automation.objects.get(month=month,year=year)
                form = MessAutomationForm(instance = log)
                return render(request, 'hab_app/automation_new_entry.html',{'form':form,'permission2':permission2,  'objects':objects_all})
        if request.GET.get('param3'):
                mth_yr = request.GET.get('param3')
                mth = mth_yr.split('_')
                month = int(mth[0])
                year = int(mth[1])
                if len(Automation.objects.filter(month=month, year = year)) > 0:
                    Automation.objects.filter(month=month, year = year).delete()

        form = MessAutomationForm()
        return render(request, 'hab_app/automation.html',{'form':form,'permission2':permission2,  'objects':objects_all})




    if request.method == 'POST' and 'btn1' in request.POST:
        form = MessAutomationForm()
        return render(request, 'hab_app/automation_new_entry.html',{'form':form,'permission2':permission2})

    if request.method == 'POST' and 'btn2' in request.POST:
        form = MessAutomationForm(data=request.POST)
        if len(Automation.objects.filter(month=request.POST['month'], year = request.POST['year'])) > 0:
            Automation.objects.filter(month=request.POST['month'], year = request.POST['year']).delete()
        if form.is_valid():
            form.save()
            objects_all  = Automation.objects.all()
            return render(request, 'hab_app/automation.html',{'form':form,'permission2':permission2,  'objects':objects_all})
        else:
            print(form.errors)





#exporting files Views
#   FEEDBACK
def import_export_files(request):
    if request.method == 'GET':
        form = MessImportExportFilesForm
        return render(request, 'hab_app/import_export_files.html',{'form':form,'permission2':1})

    queryDict = request.POST
    queryset = MessFeedback.objects.filter(hostelName=queryDict['hostelName'], month=queryDict['month'], year=queryDict['year'])
    # print(queryset)
    permission2=1

    if request.method == 'POST' and 'btn1' in request.POST:
        messfeedback_resource = MessFeedbackResource()
        dataset = messfeedback_resource.export(queryset)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mess_feedbacks.csv"'
        return response

    if request.method == 'POST' and 'btn2' in request.POST:
        messfeedback_resource = MessFeedbackResource()
        dataset = messfeedback_resource.export(queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="mess_feedbacks.xls"'
        return response

    if request.method == 'POST' and 'btn3' in request.POST:
    #preference
        preference_resource = PreferenceResource(queryset)
        dataset = preference_resource.export()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mess_preferences.csv"'
        return response

    if request.method == 'POST' and 'btn4' in request.POST:
        preference_resource = PreferenceResource()
        dataset = preference_resource.export(queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="mess_preferences.xls"'
        return response

    #imorting files as csv
    #PREFERENCE
    if request.method == 'POST' and 'btn5' in request.POST:
        final_preference_resource = FinalPreferenceResource()
        dataset = Dataset()
        new_final_preference = request.FILES['myfile']
        print(new_final_preference)
        imported_data = dataset.load(new_final_preference.read().decode('utf-8'))
        print(imported_data)
        result = final_preference_resource.import_data(dataset, dry_run=True)
        # print(result)
        if not result.has_errors():
            final_preference_resource.import_data(dataset, dry_run=False)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
 #hello rajas!!! hacktoberfest           
            
