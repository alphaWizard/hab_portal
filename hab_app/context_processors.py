from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from hab_app.models import *
from datetime import *
from django.apps import apps
from hab_app.forms import *


def metadata_processor(request):
 hostels = AllHostelMetaData.objects.all()
 return {'hostels': hostels}
