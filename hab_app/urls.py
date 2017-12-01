from django.conf.urls import url
from hab_app import views
from django.contrib import admin
app_name = 'hab_app'

urlpatterns = [
    url(r'^index/$', views.index,name='index'),
    url(r'^login/$', views.user_login,name='user_login'),
    url(r'^vacate/$', views.vacate,name='vacate'),
    url(r'^allot/$', views.allot,name='allot'),
    url(r'^home/$', views.home,name='home'),
    url(r'^chrApproveApplication/$', views.chrApproveApplication,name='chrApproveApplication'),
    url(r'^chrDisapproveApplication/$', views.chrDisapproveApplication,name='chrDisapproveApplication'),
    url(r'^showDetails/$', views.showDetails,name='showDetails'),
    url(r'^showDetails2/$', views.showDetails2,name='showDetails2'),
    url(r'^addDetails/$', views.addDetails,name='addDetails'),
    url(r'^chrAllot/$', views.chrAllot,name='chrAllot'),
    url(r'^approveApplication/$', views.approveApplication,name='approveApplication'),
    url(r'^disapproveApplication/$', views.disapproveApplication,name='disapproveApplication'),
    url(r'^generalAllot/$', views.generalAllot,name='generalAllot'),
    url(r'^trackApplication/$', views.trackApplication,name='trackApplication'),
    url(r'^deleteDetails/$', views.deleteDetails,name='deleteDetails'),
    url(r'^existingOccupants/$', views.existingOccupants,name='existingOccupants'),
    url(r'^roomDetails/$', views.roomDetails,name='roomDetails'),
    url(r'^chrViewRoom/$', views.chrViewRoom,name='chrViewRoom'),
]
