from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from datetime import datetime
# from iitgauth.views import WebmailLoginView
from .models import *
from datetime import datetime

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.contrib.auth.models import User
from .forms import *
from poplib import *

from hab_app.models import *
from django.core.urlresolvers import reverse


def manual_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_server = request.POST.get('login_server')
        em = '%s@iitg.ernet.in' % (username)
        mail = POP3_SSL(login_server)
        mail.user(username)
        try:
            mail.pass_(password)
            mail.quit()
        except:
            return HttpResponse("Invalid Webmail Credentials")
        user, created = User.objects.get_or_create(username=username, email=em)
        if created:
            user.set_password(password) # This line will hash the password
            user.save() #DO NOT FORGET THIS LINE
        # if User.objects.filter(username=username).count() == 1:
        #     user = User.objects.get(username=username)
        # else:
        #     user = User.objects.create(username=username,password=password)
        # user.username = username
        # user.password = password
        # user.login_server = login_server
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                request.session['password'] = password
                request.session['server'] = login_server
                return redirect('home')
            else:
                return HttpResponse("account not active")
        else:
            return HttpResponse("Invalid Login Credentials")
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'student_portal/login.html', {'form':form})

    # toggle below 3 lines comment status to make login necessary
# class HomeView(LoginRequiredMixin, TemplateView):
# class HomeView(TemplateView):
#     # login_url = reverse_lazy('login')
#     template_name = 'student_portal/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(HomeView, self).get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context



@login_required
def manual_logout(request):
    logout(request)
    return redirect('student_portal/login')

        # end of Views for Webmail Login



class NewFeedback(FormView):
    template_name = "student_portal/messfeedback_form.html"
    form_class = NewFeedbackForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewFeedback, self).form_valid(form)

    def get_success_url(self, *args, **kargs):
        return reverse_lazy('update_feedback')
    # def get(self, request):
    #     tags=['Hostel','User','Cleanliness and Hygiene','Breakfast','Lunch','Dinner','Catering']
    #     tag_count=0
    #
    #     for field in :
    #         field.label_tag = tags[tag_count]
    #         tag_count = tag_count+1;


curr_year = datetime.now().year
m1 = curr_month
y1 = curr_year
m1 = m1 - 1
m1_y1 = ""
if m1 < 1:
    m1 = 12
    y1 = y1 - 1
m1_y1 = str(m1) + '_' + str(y1)
class UpdateFeedback(UpdateView):

    model = MessFeedback
    form_class = NewFeedbackForm
    template_name = "student_portal/messfeedback_form.html"

    def get_object(self, *args, **kwargs):
        user_feedback = get_object_or_404(MessFeedback,username=self.request.user, month_year=m1_y1 )
        return user_feedback

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('home')

# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="check_filled_feedback",
#     ignore_result=True
# )
def check_filled_feedback(request):
    # use m1, y1, uname to check distinct
    uname = request.user
    # request.POST['user']
    # fbform = MessFeedback.objects.get(username=uname) #,month=curr_month,year=curr_year
    if MessFeedback.objects.filter(username=uname).count() == 0:
        # how to pass parameters...
        return redirect('new_feedback')
    if MessFeedback.objects.filter(username=uname).count() == 1:
        # how to pass parameters...
        if MessFeedback.objects.filter(username=uname,month=m1,year=y1).count() == 1:
            return redirect('update_feedback')
        else:
            return redirect('new_feedback')

    #ideally this should not happen
    return redirect('home')

Month_dict = {1:'january', 2:'feburary', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july', 8:'august', 9:'september', 10:'october', 11:'novermber', 12:'december'}
preference_month = (curr_month + 1)
if preference_month > 12:
    preference_month = 1

class NewPreference(FormView):
    form_class = NewPreferenceForm
    mess_on_off_list = Automation.objects.all().values()[0]

    if not mess_on_off_list[Month_dict[preference_month]] :
        template_name = "student_portal/preference_form.html"
    else:
        template_name = "student_portal/preference_form_halt.html"

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewPreference, self).form_valid(form)

    def get_success_url(self, *args, **kargs):
        return reverse_lazy('home')

    # def model_form_upload(request):
    #     if request.method == 'POST':
    #         form = DocumentForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('home')
    #     else:
    #         form = DocumentForm()
    #     return render(request, 'student_portal/messfeedback_form.html', {
    #         'form': form
    #     })
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    # Find out which variable would be storing the fields value
# See once line no.826 in django/forms/fields.py

class UpdatePreference(UpdateView):

    model = Preference
    form_class = NewPreferenceForm
    template_name = "student_portal/preference_form.html"
    def get_object(self, *args, **kwargs):
        user_preference = get_object_or_404(Preference,username=self.request.user, month_year=m1_y1 )
        return user_preference

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('home')

def check_filled_preference(request):
    # use m2, y2, uname to check distinct
    # Extract current mess subscription from HAB database
    return redirect('new_preference')


##  update information by student

def updateinfo(request):
    student_webmail=str(request.user.username)
    student = OccupantDetails.objects.filter(webmail=student_webmail).first()
    #return HttpResponse(student.name)
    if request.method == 'POST':
        form = updateinfoform(request.POST, instance=student)
        if form.is_valid():
            student.name = form.cleaned_data.get('name')
            student.idType = form.cleaned_data.get('idType')
            student.idNo = form.cleaned_data.get('idNo')
            student.gender = form.cleaned_data.get('gender')
            student.saORda = form.cleaned_data.get('saORda')
            student.altEmail = form.cleaned_data.get('altEmail')
            student.mobNo = form.cleaned_data.get('mobNo')
            student.emgercencyNo = form.cleaned_data.get('emgercencyNo')
            student.photo = form.cleaned_data.get('photo')
            student.idPhoto = form.cleaned_data.get('idPhoto')
            student.Address = form.cleaned_data.get('Address')
            student.Pincode = form.cleaned_data.get('Pincode')
            student.bankName = form.cleaned_data.get('bankName')
            student.bankAccount = form.cleaned_data.get('bankAccount')
            student.IFSCCode = form.cleaned_data.get('IFSCCode')
            student.accHolderName = form.cleaned_data.get('accHolderName')
            student.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = updateinfoform(instance = student)
    return render(request, 'student_portal/edit_details.html' , {'form': form})
    #return HttpResponse(404)
