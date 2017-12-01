from django import forms
from django.contrib.auth.models import User
from hab_app.models import *

class UpcomingOccupantForm(forms.ModelForm):
    class Meta():
        model = UpcomingOccupant
        fields = ('occupantName','idType','occupantId','hostelName','roomNo','fromStay','toStay')
        toStay = forms.DateField(widget = forms.DateTimeInput())
        fromStay = forms.DateField(widget = forms.DateTimeInput())

class UpcomingOccupantRequestForm(forms.ModelForm):
    class Meta():
        model = UpcomingOccupantRequest
        exclude =('isApprovedChr','isApprovedFirst','hostelName',)
        From_Date = forms.DateField(widget = forms.DateTimeInput())
        To_Date = forms.DateField(widget = forms.DateTimeInput())



class HostelRoomOccupantRelationForm(forms.ModelForm):
    class Meta():
        model = HostelRoomOccupantRelation
        exclude = ('toMess','fromMess')
        toRoomStay = forms.DateField(widget = forms.DateTimeInput())
        fromRoomStay = forms.DateField(widget = forms.DateTimeInput())

class OccupantDetailsForm(forms.ModelForm):
    photo = forms.ImageField(label='Choose Image' , required=False)
    idPhoto = forms.ImageField(label='Choose Image' , required=False)
    class Meta():
        model = OccupantDetails
        exclude = ('idNo',)
