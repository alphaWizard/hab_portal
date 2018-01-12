from django import forms
from django.contrib.auth.models import User
from hab_app.models import *

class UpcomingOccupantForm(forms.ModelForm):
    toStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    fromStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupant
        fields = ('occupantName','idType','occupantId','hostelName','roomNo','fromStay','toStay')


class UpcomingOccupantRequestForm(forms.ModelForm):
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    From_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    To_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupantRequest
        exclude =('isApprovedChr','hostelName','comments',)


class UpcomingOccupantRequestChrForm(forms.ModelForm):
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    From_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    To_Date = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = UpcomingOccupantRequest
        exclude =('isApprovedChr',)




class HostelRoomOccupantRelationForm(forms.ModelForm):
    toRoomStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    fromRoomStay = forms.DateField(widget = forms.DateInput(format='%m/%d/%Y'), input_formats=('%m/%d/%Y',))
    class Meta():
        model = HostelRoomOccupantRelation
        exclude = ('toMess','fromMess')


class OccupantDetailsForm(forms.ModelForm):
    photo = forms.ImageField(label='Choose Image' , required=False)
    idPhoto = forms.ImageField(label='Choose Image' , required=False)
    class Meta():
        model = OccupantDetails
        exclude = ('idNo',)

# MESS automation
class MessAutomationForm(forms.ModelForm):
    jan_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    january = forms.BooleanField(required=False)
    feb_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    feburary = forms.BooleanField(required=False)
    mar_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    march = forms.BooleanField(required=False)
    apr_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    april = forms.BooleanField(required=False)
    may_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    may = forms.BooleanField(required=False)
    jun_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    june = forms.BooleanField(required=False)
    july_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    july = forms.BooleanField(required=False)
    aug_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    august = forms.BooleanField(required=False)
    sept_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    september = forms.BooleanField(required=False)
    oct_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    october = forms.BooleanField(required=False)
    nov_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    november = forms.BooleanField(required=False)
    dec_range = forms.DateField(widget = forms.DateTimeInput(attrs={'class' : 'form-control pull-right'}))
    december = forms.BooleanField(required=False)
    class Meta():
        model = Automation
        exclude = ('month','year')
    def clean_date(self):
        jan_rangedate = self.cleaned_data['date']
        if jan_rangedate < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
