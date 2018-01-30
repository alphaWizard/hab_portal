from django import forms
from .models import *
LOGIN_SERVERS = [
    ('202.141.80.9', 'Namboor'),
    ('202.141.80.10', 'Disang'),
    ('202.141.80.11', 'Tamdil'),
    ('202.141.80.12', 'Teesta'),
    ('202.141.80.13', 'Dikrong'),
]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, label='Webmail')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    login_server = forms.ChoiceField(choices=LOGIN_SERVERS)

class NewFeedbackForm(forms.ModelForm):
    class Meta:
        model = MessFeedback
        widgets = {
          'comment': forms.Textarea(attrs={'rows':6, 'cols':100}),
        }
        fields  = ['hostelName' , 'month', 'year', 'cleanliness','qual_b','qual_l', 'qual_d','catering','comment','description', 'document',]

    def save(self, username=None):
        feedback_form = super(NewFeedbackForm, self).save(commit=False)
        if username:
            feedback_form.username = username
        feedback_form.save()
        return feedback_form


class NewPreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['hostelName','h1','h2','h3','month','year']

    def save(self, username=None):
        preference_form = super(NewPreferenceForm, self).save(commit=False)
        if username:
            preference_form.username = username
        preference_form.save()
        return preference_form

class GenSecFeedbackForm(forms.ModelForm):
    class Meta:
        model = Opi_calculated
        fields = ['raw_materials_quality']


#edit student details

from hab_app.models import *
class updateinfoform(forms.ModelForm):
    required_css_class = 'required'
    photo = forms.ImageField(label='Photo' , required=False)
    idPhoto = forms.ImageField(label='Id Photo' , required=False)
    idNo = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    idType = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta():
        model = TemporaryDetails
        exclude = ('webmail','flag','ct_approval','comments','created','updated',)
