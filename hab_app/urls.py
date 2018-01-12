from django.conf.urls import url
from hab_app import views
from django.contrib import admin
app_name = 'hab_app'
from django.conf.urls.static import static
from hab_portal import settings
urlpatterns = [
    url(r'^login/$', views.user_login,name='user_login'),
    url(r'^login_page/$', views.login_page,name='login_page'),
    url(r'^vacate/$', views.vacate,name='vacate'),
    url(r'^allot/$', views.allot,name='allot'),
    url(r'^chrApproveApplication/$', views.chrApproveApplication,name='chrApproveApplication'),
    # url(r'^chrDisapproveApplication/$', views.chrDisapproveApplication,name='chrDisapproveApplication'),
    url(r'^showDetails/$', views.showDetails,name='showDetails'),
    url(r'^showDetails2/$', views.showDetails2,name='showDetails2'),
    url(r'^addDetails/$', views.addDetails,name='addDetails'),
    url(r'^addDetails2/$', views.addDetails2,name='addDetails2'),
    url(r'^chrAllot/$', views.chrAllot,name='chrAllot'),
    # url(r'^approveApplication/$', views.approveApplication,name='approveApplication'),
    # url(r'^disapproveApplication/$', views.disapproveApplication,name='disapproveApplication'),
    url(r'^generalAllot/$', views.generalAllot,name='generalAllot'),
    url(r'^trackApplication/$', views.trackApplication,name='trackApplication'),
    url(r'^deleteDetails/$', views.deleteDetails,name='deleteDetails'),
    url(r'^existingOccupants/$', views.existingOccupants,name='existingOccupants'),
    url(r'^roomDetails/$', views.roomDetails,name='roomDetails'),
    url(r'^chrViewRoom/$', views.chrViewRoom,name='chrViewRoom'),
    url(r'^chrHostelSummary/$', views.chrHostelSummary,name='chrHostelSummary'),
    url(r'^chrCaretakerView/$', views.chrCaretakerView,name='chrCaretakerView'),
    url(r'^chrFreshersBulkAllot/$',views.chrFreshersBulkAllot, name='chrFreshersBulkAllot'),

    
    url(r'^mess_opi/$', views.mess_opi,name='mess_opi'),
    url(r'^mess_opi/calculate$', views.opi_calculate,name='opi_calculate'),
    url(r'^mess_automation/$', views.mess_automation,name='mess_automation'),
    url(r'^mess_automation/messfeedback_export_csv/$', views.export_feedback_as_csv,name='export_feedback_as_csv'),
    url(r'^mess_automation/messfeedback_export_xls/$', views.export_feedback_as_xls,name='export_feedback_as_xls'),
    url(r'^mess_automation/preference_export_csv/$', views.export_preference_as_csv,name='export_preference_as_csv'),
    url(r'^mess_automation/preference_export_xls/$', views.export_preference_as_xls,name='export_preference_as_xls'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
