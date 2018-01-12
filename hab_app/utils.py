import requests
from student_portal.models import *
from django.shortcuts import render,redirect

def opi_calculate():
    feedbacks = MessFeedback.objects.all()
    print(feedbacks)
    hostelss = []
    noh = 0         # number of hostels
    freq_hostelss = []  #hostel wise freq of the feedback
    for fb in feedbacks:
        #   count No. of feedbacks hostelwise
        if fb.hostelName not in hostelss:
            hostelss.append(fb.hostelName)
            noh = noh + 1
            freq_hostelss.append(1)
        else:
            freq_hostelss[hostelss.index(fb.hostelName)] += 1

#   one loop to calculate sum of 5 fields hostelwise and then take their average
    opis = [0] * len(hostelss)
    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = (fb.cleanliness + fb.qual_b + fb.qual_l + fb.qual_d + fb.catering)/5
    print(opis)
    for fb in feedbacks:
        opis[hostelss.index(fb.hostelName)] = opis[hostelss.index(fb.hostelName)] / freq_hostelss[hostelss.index(fb.hostelName)]
    Opi_calculated.objects.all().delete()
    for i in range(len(opis)):
        opi_object = Opi_calculated(hostelName=hostelss[i])
        opi_object.opi_value = opis[i]
        opi_object.numberOfSubscriptions = freq_hostelss[i]
        opi_object.save()
    print('Opi Calculated')
    return redirect('hab_app:mess_opi')
