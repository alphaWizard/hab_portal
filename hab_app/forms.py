from django import forms
from django.contrib.auth.models import User
from hab_app.models import *
from django.apps import apps

from django.forms import ModelChoiceField

class UpcomingOccupantForm(forms.ModelForm):
    required_css_class = 'required'
    toStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    fromStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupant
        fields = ('occupantName','idType','occupantId','hostelName','roomNo','fromStay','toStay','comments')


class UpcomingOccupantRequestForm(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    From_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    To_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupantRequest
        exclude =('isApprovedChr','hostelName','comments',)


class UpcomingOccupantRequestChrForm(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    From_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    To_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupantRequest
        exclude =('isApprovedChr',)




class HostelRoomOccupantRelationForm(forms.ModelForm):
    required_css_class = 'required'
    hostelName = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    toRoomStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    fromRoomStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = HostelRoomOccupantRelation
        exclude = ('toMess','fromMess')


class OccupantDetailsForm(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    class Meta():
        model = OccupantDetails
        exclude = ('idNo','flag')

class OccupantDetailsEditForm(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    class Meta():
        model = OccupantDetails
        exclude = ('flag',)

class CtApproveStudentEditForm(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='photo' , required=False)
    idPhoto = forms.ImageField(label='idPhoto' , required=False)
    class Meta():
        model = TemporaryDetails
        exclude = ('ct_approval','flag','created','updated')




GENDER_CHOICES =(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)
STATUS_CHOICES =(
    ('Pending','Pending'),
    ('Approved','Approved'),
    ('Disapproved','Disapproved'),
)
FLOOR_CHOICES =(
    ('Ground Floor','Ground Floor'),
    ('First Floor','First Floor'),
    ('Second Floor','Second Floor'),
    ('Third Floor','Third Floor'),
    ('Fourth Floor','Fourth Floor'),
)
ROOM_STATUS_CHOICES =(
    ('Usable','Usable'),
    ('Abandoned','Abandoned'),
    ('Partially Damaged','Partially Damaged'),
)

HOSTEL_CHOICES = (
        ('Barak', 'Barak'),
        ('Bramhaputra', 'Bramhaputra'),
        ('Dhansiri', 'Dhansiri'),
        ('Dibang', 'Dibang'),
        ('Dihing', 'Dihing'),
        ('Kameng', 'Kameng'),
        ('Kapili', 'Kapili'),
        ('Lohit', 'Lohit'),
        ('Manas', 'Manas'),
        ('Siang', 'Siang'),
        ('Subansiri', 'Subansiri'),
        ('Umiam', 'Umiam'),
    )
##room details edit

class chrRoomDetailsEditForm(forms.Form):
    roomNo = forms.CharField(max_length=255)
    roomOccupancyType =  forms.ModelChoiceField(queryset=RoomCategory.objects.all(), empty_label=None)
    floorInfo = forms.ChoiceField(choices = FLOOR_CHOICES)
    roomStatus = forms.ChoiceField(choices=ROOM_STATUS_CHOICES)
    roomOccupancyGender = forms.ChoiceField(choices=GENDER_CHOICES)
    comments = forms.CharField(max_length=255,required =False)




# MESS automation
class MessAutomationForm(forms.ModelForm):

    # jan_fb_start_date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y',attrs={'class' : 'form-control pull-right'}), input_formats=('%m/%d/%Y',))
    # jan_fb_end_date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y',attrs={'class' : 'form-control pull-right'}), input_formats=('%m/%d/%Y',))
    # jan_pf_start_date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y',attrs={'class' : 'form-control pull-right'}), input_formats=('%m/%d/%Y',))
    # jan_pf_end_date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y',attrs={'class' : 'form-control pull-right'}), input_formats=('%m/%d/%Y',))
    # # january = forms.BooleanField()

    feed_start_date= forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    feed_off_date= forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))

    pref_start_date= forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    pref_off_date= forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))

    class Meta():
        model = Automation
        exclude = ()
    def clean_date(self):
        jan_fb_start_date = self.cleaned_data['date']
        if jan_fb_start_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
class MessImportExportFilesForm(forms.ModelForm):
    class Meta():
        model = ImportExportFiles
        exclude = ()
