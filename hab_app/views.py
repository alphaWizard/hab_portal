from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
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
    request.session['server'] = "abc"
    if request.session['username'] == "chr_hab":
        permission2 = 1
        hostels = AllHostelMetaData.objects.all()
        return render(request,'hab_app/chrView.html',{'permission2':permission2})
    elif request.session['username'][-3:]== "off":
        username = request.session['username'][:-3]
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = username)
        return render(request,'hab_app/caretakerView.html',{'ROtable':ROtable})
    elif CaretakerViewAccess.objects.filter(webmail = request.session['username']).count()==1:
        permission2 = 0
        hostels = AllHostelMetaData.objects.all()
        return render(request,'hab_app/chrView.html',{'permission2':permission2})
    elif request.session['server']=="202.141.80.13" :
        return render(request,'student_portal/home.html')
    else:
        return render(request,'hab_app/generalView.html')


def login_page(request):
    return render(request,'hab_app/login.html')

@login_required
def logout1(request):
    logout(request)
    return redirect('hab_app:login_page')


def showDetails(request):
    permission = 1
    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
        permission = 0
    else:
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
    if request.method == 'GET':
        parameter = request.GET.get('param')
        details = OccupantDetails.objects.get(idNo = parameter)
        temp = ROtable.hostelRoomOccupant
        mymodel = apps.get_model(app_label='hab_app', model_name=temp)
        roDetails = mymodel.objects.get(occupantId__iexact = parameter)
        return render(request,'hab_app/showDetails.html',{'ROtable':ROtable,'details':details,'roDetails':roDetails,'permission':permission})

def showDetails2(request):
    if request.method == 'GET':
        parameter = request.GET.get('param')
        pobj = OccupantDetails.models.get(idNo=parameter)
        details = OccupantDetails.objects.get(idNo = parameter)
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
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
    permission = 1
    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
        permission = 0
    else:
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
    temp = ROtable.hostelRoomOccupant
    mymodel = apps.get_model(app_label='hab_app', model_name=temp)
    now = datetime.now()
    start = now - timedelta(days=4)
    end = now + timedelta(days=4)
    tobeVacated = mymodel.objects.filter(toRoomStay__range=(start.date(),end.date()))
    for i in tobeVacated:
        temp1 = OccupantDetails.objects.get(idNo__iexact = i.occupantId)
        i.name = temp1.name
        i.contact = temp1.mobNo
    return render(request,'hab_app/vacate.html',{'ROtable':ROtable,'tobeVacated':tobeVacated,'permission':permission})


def allot(request):
    permission = 1
    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = request.session['hostel_view'])
        tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = request.session['hostel_view'],isApprovedChr="Approved")
        permission = 0
    else:
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = request.session['username'][:-3])
        tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = request.session['username'][:-3],isApprovedChr="Approved")
    return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted,'tobeAlloted2':tobeAlloted2,'permission':permission})


def chrAllot(request):
    permission2=1
    hostels = AllHostelMetaData.objects.all()
    if request.method == 'POST':
        form = UpcomingOccupantForm(data=request.POST)
        if form.is_valid:
            occupant = form.save()
            occupant.save()
            form = UpcomingOccupantForm()
            return render(request,'hab_app/addOccupant.html',{'form':form,'permission2':permission2})
        else:
            print(form.errors)

    else:
        form = UpcomingOccupantForm()
        return render(request,'hab_app/addOccupant.html',{'form':form,'permission2':permission2})

def addDetails(request):
    permission = 1
    if request.session['hostel_view']!="a1x":
        permission = 0
    ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
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


            if form2.is_valid:
                instance = form2.save(commit=False)
                instance.idNo = occupantId
                instance.save()
            else:
                print(form2.errors)
        else:
            print(form1.errors)
        log = UpcomingOccupant.objects.get(occupantId = occupantId).delete()
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = request.session['username'][:-3])
        return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted,'permission':'permission'})

    if request.method == 'GET':

        occupantId = request.GET.get('param')
        tobeAlloted = UpcomingOccupant.objects.get(occupantId = occupantId)
        initialData1 = {'occupantId': tobeAlloted.occupantId,'hostelName': tobeAlloted.hostelName,'roomNo': tobeAlloted.roomNo,'fromRoomStay': tobeAlloted.fromStay,'toRoomStay': tobeAlloted.toStay}
        initialData2 = {'name':tobeAlloted.occupantName,'idType':tobeAlloted.idType}
        form1 = HostelRoomOccupantRelationForm(initial = initialData1)
        form2 = OccupantDetailsForm(initial = initialData2)
        return render(request,'hab_app/temp.html',{'form1':form1,'form2':form2,'permission':'permission'})

def addDetails2(request):
    permission = 1
    if request.session['hostel_view']!="a1x":
        permission = 0
    ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
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

            if form2.is_valid:
                instance = form2.save(commit=False)
                instance.idNo = occupantId
                instance.save()
            else:
                print(form2.errors)
        else:
            print(form1.errors)
        log = UpcomingOccupantRequest.objects.get(id_no = occupantId,isApprovedChr="Approved").delete()
        tobeAlloted = UpcomingOccupant.objects.filter(hostelName__iexact = request.session['username'][:-3])
        tobeAlloted2 = UpcomingOccupantRequest.objects.filter(hostelName__iexact = request.session['username'][:-3],isApprovedChr="Approved")
        return render(request,'hab_app/allot.html',{'ROtable':ROtable,'tobeAlloted':tobeAlloted,'tobeAlloted2':tobeAlloted2,'permission':'permission'})

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
        return render(request,'hab_app/temp.html',{'form1':form1,'form2':form2,'permission':'permission'})

def deleteDetails(request):
    permission = 1
    if request.method == 'GET':
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
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
        return render(request,'hab_app/vacate.html',{'ROtable':ROtable,'tobeVacated':tobeVacated,'permission':permission})

@cache_page(20)
def existingOccupants(request):
    permission = 1
    if request.session['hostel_view']!="a1x":
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
        permission = 0
    else:
        ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
    temp = ROtable.hostelRoomOccupant
    mymodel = apps.get_model(app_label='hab_app', model_name=temp)
    relation = mymodel.objects.all()
    occupants = list()
    for i in relation:
        if OccupantDetails.objects.filter(idNo__iexact=i.occupantId).exists():
            occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
    zipped = zip(relation,occupants)
    return render(request,'hab_app/existingOccupants.html',{'ROtable':ROtable,'zipped':zipped,'permission':permission})

@cache_page(20)
def roomDetails(request):
    if request.method == 'GET':
        index = request.GET.get('param')
        #occupied rooms
        #get the relation table name and room table name
        permission = 1
        if request.session['hostel_view']!="a1x":
            ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['hostel_view'])
            permission = 0
        else:
            ROtable = AllHostelMetaData.objects.get(hostelName__iexact = request.session['username'][:-3])
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
                occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
                if room_model.objects.filter(roomNo = i.roomNo).exists():
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
            return render(request,'hab_app/occupiedRooms.html',{'ROtable':ROtable,'zipped':zipped,'permission':permission})

        elif index == "2":
            #empty rooms
            return render(request,'hab_app/emptyRooms.html',{'ROtable':ROtable,'empty_rooms':empty_rooms,'permission':permission})

        else:
            return render(request,'hab_app/totalRooms.html',{'ROtable':ROtable,'zipped':zipped ,'empty_rooms':empty_rooms,'permission':permission})



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
    permission2=1
    hostels = AllHostelMetaData.objects.all()
    if request.method == 'GET':
        if request.GET.get('param') :
            idNo = request.GET.get('param')
            guest = UpcomingOccupantRequest.objects.get(id_no = idNo,isApprovedChr="Pending")
            form =UpcomingOccupantRequestChrForm(instance=guest)
            return render(request,"hab_app/chrApproveEdit.html",{'form':form,'permission2':permission2,'guest':guest})
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
    return render(request,"hab_app/chrApproveApplication.html",{'applicants':applicants,'permission2':permission2})


# def chrDisapproveApplication(request):
#     permission2=1
#     if request.method == 'GET':
#         if request.GET.get('param') :
#             idNo = request.GET.get('param')
#             # guest = UpcomingOccupantRequest.objects.get(id_no = idNo,isApprovedChr="Pending")
#             # guest.isApprovedChr = "Disapproved"
#             # guest.save()
#
#     applicants = UpcomingOccupantRequest.objects.filter(isApprovedChr = "Pending" )
#     return render(request,"hab_app/chrApproveApplication.html",{'applicants':applicants,'permission2':permission2})

@cache_page(20)
def chrViewRoom(request):
    permission2 = 1

    if request.session['username'] != "chr_hab":
        permission2 = 0

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
                    occupants.append(OccupantDetails.objects.get(idNo__iexact=i.occupantId))
                    if room_model.objects.filter(roomNo = i.roomNo).exists():
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
            return render(request,'hab_app/chrViewRoom.html',{'ROtable':ROtable,'zipped':zipped ,'empty_rooms':empty_rooms,'permission2':permission2})

@cache_page(20)
def chrHostelSummary(request):
    permission2 = 1

    if request.session['username'] != "chr_hab":
        permission2 = 0

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
    return render(request,'hab_app/chrHostelSummary.html',{'zipped_summary':zipped_summary,'total':total,'permission2':permission2})



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
    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = (fb.cleanliness + fb.qual_b + fb.qual_l + fb.qual_d + fb.catering)/5
    print(opis)
    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = opis[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
    Opi_calculated.objects.filter(month=m111,year=y111).delete()
    for i in range(len(opis)):
        opi_object = Opi_calculated(hostelName=hostelss[i])
        opi_object.opi_value = opis[i]
        opi_object.numberOfSubscriptions = freq_hostelss[i]
        opi_object.save()
    print('Opi Calculated')
    return redirect('hab_app:mess_opi')

def mess_automation(request):
    permission2=1
    if request.method == 'GET':
        temp = Automation.objects.all()
        form = MessAutomationForm(initial= temp.values()[0])
        return render(request, 'hab_app/automation.html',{'form':form,'permission2':permission2})
    if request.method == 'POST' and 'btn1' in request.POST:
        form = MessAutomationForm(request.POST)
        if form.is_valid():
            abc=Automation.objects.all().delete()
            instance = form.save(commit=False)
            instance.month = m1
            instance.year = y1
            instance.save()
            temp = Automation.objects.all()
            form = MessAutomationForm(initial= temp.values()[0])

    #imorting files as csv
    #PREFERENCE
    if request.method == 'POST' and 'btn2' in request.POST:
        form = MessAutomationForm(request.POST)
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

    return render(request, 'hab_app/automation.html',{'form':form,'permission2':permission2})

#exporting files Views
#   FEEDBACK
def export_feedback_as_csv(request):
    messfeedback_resource = MessFeedbackResource()
    dataset = messfeedback_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mess_feedbacks.csv"'
    return response

def export_feedback_as_xls(request):
    messfeedback_resource = MessFeedbackResource()
    dataset = messfeedback_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mess_feedbacks.xls"'
    return response
#   PREFERENCE
def export_preference_as_csv(request):
    preference_resource = PreferenceResource()
    dataset = preference_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mess_preferences.csv"'
    return response

def export_preference_as_xls(request):
    preference_resource = PreferenceResource()
    dataset = preference_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mess_preferences.xls"'
    return response
