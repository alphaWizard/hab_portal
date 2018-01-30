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
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import datetime
# from iitgauth.views import WebmailLoginView
from .models import *
from datetime import datetime

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task

from django.contrib.auth.models import User
from .forms import *
from poplib import *

from hab_app.models import *
from django.core.urlresolvers import reverse

curr_year = datetime.now().year
curr_month = datetime.now().month
m1 = curr_month
y1 = curr_year
m1 = m1 - 1
m1_y1 = ""
if m1 < 1:
    m1 = 12
    y1 = y1 - 1
m1_y1 = str(m1) + '_' + str(y1)

m2 = curr_month
y2 = curr_year
m2 = m2 + 1
m2_y2 = ""
if m2 > 12:
    m2 = 1
    y2 = y2 + 1
m2_y2 = str(m2) + '_' + str(y2)

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
@login_required
def get_initial(request):
    #initial = super(NewFeedback, self).get_initial()
    initial  = { 'baseHostel':'', 'subscribedHostel' :''  }
    ocupant_user_id_dict = OccupantDetails.objects.filter(webmail=request.user).values_list('idNo')
    # ocupant_user_id = ocupant_user_id_dict['idNo']
    if len(ocupant_user_id_dict) == 1 :
        value_id = list(map(str, ocupant_user_id_dict.first()))[0]        # use map(str, ocupant_user_id_dict.first()) in case of python2
        # print(value_id)
        occupant_hostel = []
        if not BarakRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(BarakRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not BramhaputraRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(BramhaputraRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not DhansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(DhansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not DibangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(DibangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not DihingRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(DihingRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not KamengRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(KamengRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not LohitRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(LohitRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not ManasRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(ManasRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not SubansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(SubansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

        if not UmiamRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
            occupant_hostel.append(UmiamRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())
        # print(SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first()[0])
        # occupant_hostel += KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName')
        # print(SiangRORelation.objects.all())

        if len(occupant_hostel) == 1 :
            occupant_hostel_name = occupant_hostel[0]
            initial['baseHostel'] = occupant_hostel[0][0]

        assigned_mess = ""
        if FinalPreference.objects.filter(username=request.user, month=datetime.now().month, year=datetime.now().year):
            assigned_mess = FinalPreference.objects.filter(username=request.user, month=datetime.now().month, year=datetime.now().year)[0]
        # print(assigned_mess.hostelName)
        if assigned_mess :
            initial['subscribedHostel'] = assigned_mess.final_hostel
        else:
            initial['subscribedHostel'] = initial['baseHostel']
    # ocupant_user = OccupantDetails.objects.filter(webmail=self.request.user)


    return initial



class NewFeedback(FormView):
    template_name = "student_portal/messfeedback_form.html"
    form_class = NewFeedbackForm
    monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   
    def get(self, *args, **kwargs):
        uname = self.request.user
        # print(MessFeedback.objects.filter(username=uname,month=m1,year=y1).count())
        # print(self.request.user)
        automation_objects = Automation.objects.filter(feed_start_date__lte=datetime.today(), feed_off_date__gte=datetime.today())
        # print(automation_objects)
        if len(automation_objects) == 0 or len(automation_objects) > 1:
            feedback_ON_OFF = False
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form, 'feedback_ON_OFF': feedback_ON_OFF})

        automation_object = automation_objects[0]
        # automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)
        if MessFeedback.objects.filter(username=uname ,month=automation_object.month, year = automation_object.year).count() == 1:
            return HttpResponseRedirect('update')
        else :
            initial = get_initial(self.request)
            feed_initial = { 'hostelName' : initial['subscribedHostel'] , 'month': automation_object.month, 'year' : automation_object.year }
            feed_initial['hostelName'] = initial['subscribedHostel']
            automation_objects = Automation.objects.filter(feed_start_date__lte=datetime.today(), feed_off_date__gte=datetime.today())
            form = self.form_class(initial=feed_initial)

            feedback_ON_OFF = True
            if len(automation_objects) == 1:
                automation_object = automation_objects[0]
                # print(automation_object.feed_start_date)

                feed_on_off = automation_object.feed_on_off
                if feed_on_off == True:
                    feed_start_date = automation_object.feed_start_date
                    feed_off_date = automation_object.feed_off_date
                    if feed_start_date < datetime.now().date() and feed_off_date > datetime.now().date() :
                        feedback_ON_OFF = True
                    else:
                        feedback_ON_OFF = False
                else:
                    feedback_ON_OFF = False
            else:
                feedback_ON_OFF = False

            return render(self.request, self.template_name, {'form': form, 'feedback_ON_OFF': feedback_ON_OFF, 'mth': automation_object.month , 'yr':automation_object.year})


    # def dispach(self, request):
    #     uname = self.request.user
    #     if MessFeedback.objects.filter(username=uname,month=m1,year=y1).count() == 1:
    #         return HttpResponseRedirect('update')



    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewFeedback, self).form_valid(form)

    def get_success_url(self, *args, **kargs):
        messages.success(self.request, 'Changes are saved!!')
        return reverse_lazy('update_feedback')
    """
    def get_initial(self):
        # initial = super(NewFeedback, self).get_initial()
        initial = {'base_hostel' : '' , 'final_hostel' :''}
        ocupant_user_id_dict = OccupantDetails.objects.filter(webmail=self.request.user).values_list('idNo')
        # ocupant_user_id = ocupant_user_id_dict['idNo']
        if len(ocupant_user_id_dict) == 1 :
            value_id = list(map(str, ocupant_user_id_dict.first()))[0]        # use map(str, ocupant_user_id_dict.first()) in case of python2
            # print(value_id)
            occupant_hostel = []
            if not BarakRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(BarakRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not BramhaputraRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(BramhaputraRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not DhansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(DhansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not DibangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(DibangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not DihingRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(DihingRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not KamengRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(KamengRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not LohitRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(LohitRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not ManasRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(ManasRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not SubansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(SubansiriRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())

            if not UmiamRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first() == None :
                occupant_hostel.append(UmiamRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first())
            # print(SiangRORelation.objects.filter(occupantId=value_id).values_list('hostelName').first()[0])
            # occupant_hostel += KapiliRORelation.objects.filter(occupantId=value_id).values_list('hostelName')
            # print(SiangRORelation.objects.all())


            if len(occupant_hostel) == 1 :
                occupant_hostel_name = occupant_hostel[0]
                initial['hostelName'] = occupant_hostel[0][0]


            assigned_mess = ""
            if FinalPreference.objects.filter(username=self.request.user, month=datetime.now().month, year=datetime.now().year):
                assigned_mess = FinalPreference.objects.filter(username=self.request.user, month=datetime.now().month, year=datetime.now().year)[0]
            # print(assigned_mess.hostelName)
            if assigned_mess :
                initial['hostelName'] = assigned_mess.final_hostel
        # ocupant_user = OccupantDetails.objects.filter(webmail=self.request.user)


        return initial
        """
    # def get(self, request):
    #     tags=['Hostel','User','Cleanliness and Hygiene','Breakfast','Lunch','Dinner','Catering']
    #     tag_count=0
    #
    #     for field in :
    #         field.label_tag = tags[tag_count]
    #         tag_count = tag_count+1;



class UpdateFeedback(UpdateView):

    model = MessFeedback
    form_class = NewFeedbackForm
    template_name = "student_portal/messfeedback_form.html"

    # def get(self, request):
    #     uname = self.request.user
    #     if MessFeedback.objects.filter(username=uname,month=m1,year=y1).count() == 0:
    #         return HttpResponseRedirect('new')

    def get_object(self, *args, **kwargs):
        automation_objects = Automation.objects.filter(feed_start_date__lte=datetime.today(), feed_off_date__gte=datetime.today())
        automation_object = automation_objects[0]
        # automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)
        user_feedback = get_object_or_404(MessFeedback,username=self.request.user,  month=automation_object.month, year = automation_object.year)
        return user_feedback


    def get_context_data(self, **kwargs):

        automation_objects = Automation.objects.filter(feed_start_date__lte=datetime.today(), feed_off_date__gte=datetime.today())
        automation_object = automation_objects[0]
        # automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)
        feedback_ON_OFF  = True
        if get_object_or_404(MessFeedback,username=self.request.user,  month=automation_object.month, year = automation_object.year) :
            feedback_ON_OFF  = True
        else:
            feedback_ON_OFF  = False

        context = super().get_context_data(**kwargs)
        context['feedback_ON_OFF'] = feedback_ON_OFF
        context['mth'] = automation_object.month
        context['yr'] = automation_object.year
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('home')

# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="check_filled_feedback",
#     ignore_result=True
# )

# def checker(request):
#     uname = request.user
#     if MessFeedback.objects.filter(username=uname,month=m1,year=y1).count() == 0:
#         return HttpResponseRedirect(reverse('student_portal:new_feedback',kwargs={'user': request.user}))
#     if MessFeedback.objects.filter(username=uname,month=m1,year=y1).count() == 1:
#         return HttpResponseRedirect(reverse('student_portal:update_feedback',kwargs={'user': request.user}))

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

        automation_objects = Automation.objects.filter(feed_start_date__lte=datetime.today(), feed_off_date__gte=datetime.today())
        if len(automation_objects) == 0 or len(automation_objects) >1:
            return redirect('new_feedback')
        automation_object = automation_objects[0]
        if MessFeedback.objects.filter(username=uname,month=automation_object.month,year=automation_object.year).count() == 1:
            return redirect('update_feedback')
        else:
            return redirect('new_feedback')

    #ideally this should not happen
    return redirect('home')

Month_dict = {1:'january', 2:'feburary', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july', 8:'august', 9:'september', 10:'october', 11:'novermber', 12:'december'}
preference_month = (curr_month + 1)
preference_year = (curr_year)
if preference_month > 12:
    preference_month = 1
    preference_year += 1

class NewPreference(FormView):
    form_class = NewPreferenceForm
    template_name = "student_portal/preference_form.html"

    automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())

    # print(automation_objects)

    def get(self, request):
        uname = self.request.user
        automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
        if len(automation_objects) == 0 or len(automation_objects) > 1:
            preference_ON_OFF = False
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form, 'preference_ON_OFF': preference_ON_OFF})

        automation_object = automation_objects[0]
        #automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)

        # month=automation_object_month, year = automation_object_year) :
        if Preference.objects.filter(username=uname,month=automation_object.month,year = automation_object.year).count() == 1:
            return HttpResponseRedirect('update')
        else :
            automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
            # pref_month = automation_object.month
            # preference_year = automation_object.year
            #
            # FinalPreference.
            initial = get_initial(self.request)
            pref_dict = {'hostelName' :initial['baseHostel'] , 'month': automation_object.month , 'year':automation_object.year }

            form = self.form_class(initial=pref_dict)
            preference_ON_OFF = True
            if len(automation_objects) == 1:
                automation_object = automation_objects[0]
                print(automation_object.pref_start_date)

                pref_on_off = automation_object.pref_on_off
                if pref_on_off == True:
                    pref_start_date = automation_object.pref_start_date
                    pref_off_date = automation_object.pref_off_date
                    if pref_start_date < datetime.now().date() and pref_off_date > datetime.now().date() :
                        preference_ON_OFF = True
                    else:
                        preference_ON_OFF = False
                else:
                    preference_ON_OFF = False
            else:
                preference_ON_OFF = False
            return render(self.request, self.template_name, {'form': form, 'preference_ON_OFF': preference_ON_OFF, 'mth':automation_object.month, 'yr':automation_object.year})


    """
    def form_valid(self, form):
        automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
        automation_object = automation_objects[0]
        # print(automation_object.month)
        form.cleaned_data['month'] = automation_object.month
        form.cleaned_data['year'] = automation_object.year

        print(form.cleaned_data['month'])

        form.cleaned_data['month_year'] = str(form.cleaned_data['month']) + '_' + str(form.cleaned_data['year'])
        # form.save(self.request.user)
        pref_obj = Preference(month_year = form.cleaned_data['month_year'])
        pref_obj.month = form.cleaned_data['month']
        pref_obj.year = form.cleaned_data['year']
        pref_obj.username = self.request.user
        # pref_obj.hostelName =
        pref_obj.h1 = form.cleaned_data['h1']
        pref_obj.h2 = form.cleaned_data['h2']
        pref_obj.h3 = form.cleaned_data['h3']
        pref_obj.save()
        # return super(NewPreference, self).form_valid(form)
        return HttpResponseRedirect('update')
    """

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewPreference, self).form_valid(form)

    def get_success_url(self, *args, **kargs):
        return reverse_lazy('home')


    # Find out which variable would be storing the fields value
# See once line no.826 in django/forms/fields.py

class UpdatePreference(UpdateView):

    model = Preference
    form_class = NewPreferenceForm
    template_name = "student_portal/preference_form.html"

    def get_object(self, *args, **kwargs):
        automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
        automation_object = automation_objects[0]
        #automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)
        #print(automation_month_year)
        print(self.request.user)
        user_preference = get_object_or_404(Preference,username=self.request.user, month = automation_object.month, year=automation_object.year)
        return user_preference

    def get_context_data(self, **kwargs):
        automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
        automation_object = automation_objects[0]
        # automation_month_year = str(automation_object.month) + '_' + str(automation_object.year)
        #automation_object_year  = automation_object.year
        #automation_object_month = automation_object.month
        preference_ON_OFF  = True
        if get_object_or_404(Preference,username=self.request.user, month=automation_object.month, year = automation_object.year) :
            preference_ON_OFF  = True
        else:
            preference_ON_OFF  = False

        context = super().get_context_data(**kwargs)
        context['preference_ON_OFF'] = preference_ON_OFF
        context['mth'] = automation_object.month
        context['yr'] = automation_object.year
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('home')

def check_filled_preference(request):
    # use m2, y2, uname to check distinct
    # Extract current mess subscription from HAB database

    uname = request.user
    if Preference.objects.filter(username=uname).count() == 0:
        # how to pass parameters...
        return redirect('new_preference')
    if Preference.objects.filter(username=uname).count() > 0:
        # how to pass parameters...
        automation_objects = Automation.objects.filter(pref_start_date__lte=datetime.today(), pref_off_date__gte=datetime.today())
        if len(automation_objects) == 0:
            print('helll1')
            return redirect('new_preference')

        if len(automation_objects) == 1:
            automation_object = automation_objects[0]
            if Preference.objects.filter(username=uname,month=automation_object.month,year=automation_object.year).count() == 1:
                print('helll2')
                return redirect('update_preference')
            else:
                return redirect('new_preference')

        if len(automation_objects) > 1:
            return redirect('new_preference')


    return redirect('home')

#need to replace month_year with automation
def gensec_feedback(request):
    form = GenSecFeedbackForm()
    if request.method == 'GET':
        return render(request, 'student_portal/gensec_feedback.html', {'form': form})
    if request.method == 'POST':
        # print(form)
        # if form.is_valid():
        print(request.user)
        gensec_id = "1234567Siang"
        # gensec_id = str(request.user)
        # print(gensec_id)
        gensec_hostelname = str(gensec_id[7:])    # assuming the gensec id to be gensec.hostelname
        if Opi_calculated.objects.filter(hostelName=gensec_hostelname,month_year=m1_y1 ).count() == 0:
            opi_object = Opi_calculated(hostelName=gensec_hostelname,month_year=m1_y1)
        else:
            opi_object = Opi_calculated.objects.filter(hostelName=gensec_hostelname,month_year=m1_y1 )[0]
        # print(request.POST)
        opi_object.raw_materials_quality = request.POST['raw_materials_quality']
        opi_object.opi_value = 0.0
        opi_object.numberOfSubscriptions = 0
        opi_object.save()
        return HttpResponseRedirect(reverse('home'))
        # else:
        #     return HttpResponse("form invalid")


def gensec_info(request):
    if request.method == 'GET':
        # prev_month_feedback = Opi_calculated.objects.filter(hostelName=gensec_hostelname, month_year=m1_y1)
        #
        # no_feedbacks_prev_month = str(0)
        # no_subscriptions_prev_month = str(0)
        #
        # if len(prev_month_feedback) == 0:
        #     no_feedbacks_prev_month = 'no data found !'
        #
        #
        # no_feedbacks_prev_month =
        # no_subscriptions_prev_month =
        return render(request, 'student_portal/gensec_info.html')

#  update information by student

def updateinfo(request):

    student1 = OccupantDetails.objects.get(webmail=request.user.username)
    tobeAlloted = OccupantDetails.objects.get(webmail=request.user.username)
    if request.method == 'GET':
        # if TemporaryDetails.objects.filter(webmail=request.user.username,ct_approval="Pending").exists():
        #     return HttpResponse("You already have a Pending Request!!!")
        # student,created = TemporaryDetails.objects.get_or_create(webmail=request.user.username,ct_approval="Pending")
        initialData = {
                        'name':tobeAlloted.name,'idType':tobeAlloted.idType,
                        'gender':tobeAlloted.gender,'saORda':tobeAlloted.saORda,
                        'altEmail':tobeAlloted.altEmail,'idNo':tobeAlloted.idNo,
                        'mobNo':tobeAlloted.mobNo,'emgercencyNo':tobeAlloted.emgercencyNo,
                        'Address':tobeAlloted.Address,'Pincode':tobeAlloted.Pincode,
                        'bankName':tobeAlloted.bankName,'bankAccount':tobeAlloted.bankAccount,
                        'IFSCCode':tobeAlloted.IFSCCode,'accHolderName':tobeAlloted.accHolderName,
                        'photo':tobeAlloted.photo,'idPhoto':tobeAlloted.idPhoto,
                    }
        form = updateinfoform(initial=initialData)
        return render(request, 'student_portal/edit_details.html' , {'form': form})
    #return HttpResponse(student.name)
    if request.method == 'POST':
        if TemporaryDetails.objects.filter(webmail=request.user.username,ct_approval="Pending").exists():
            return HttpResponse("You already have a Pending Request!!!")

        form = updateinfoform(request.POST,request.FILES)
        if form.is_valid():
            temporary_data = form.save(commit=False)
            if not temporary_data.photo:
                temporary_data.photo = student1.photo
            if not temporary_data.idPhoto:
                temporary_data.idPhoto = student1.idPhoto
            temporary_data.webmail = request.user.username
            temporary_data.ct_approval = "Pending"
            temporary_data.flag = 1
            temporary_data.save()
            # messages.success(request, 'Changes are saved!!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("form invalid")
    #return HttpResponse(404)
def track(request):
    student_requests = TemporaryDetails.objects.filter(webmail=request.user.username).order_by('created')
    return render(request,'student_portal/student_track.html',{'req':student_requests})
