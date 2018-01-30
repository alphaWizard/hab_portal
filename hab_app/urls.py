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
    url(r'^caretakerapproveinfo/$', views.caretakerapproveinfo,name='caretakerapproveinfo'),
    url(r'^ct_add_occupant/$', views.ct_add_occupant,name='ct_add_occupant'),
    url(r'^chrViewSpecialRooms/$', views.chrViewSpecialRooms,name='chrViewSpecialRooms'),
    url(r'^editRODetails/$', views.editRODetails,name='editRODetails'),
    url(r'^editOccupantDetails/$', views.editOccupantDetails,name='editOccupantDetails'),
    url(r'^chrRoomDetailsEdit/$', views.chrRoomDetailsEdit,name='chrRoomDetailsEdit'),
    url(r'^chrRoomDetailsEdit2/(?P<hostel_name>[a-zA-Z0-9_]+)$', views.chrRoomDetailsEdit2 , name='chrRoomDetailsEdit2'),
    url(r'^chrRoomAdd/(?P<hostel_name>[a-zA-Z0-9_]+)$', views.chrRoomAdd,name='chrRoomAdd'),
    url(r'^chrRoomDelete/(?P<hostel_name>[a-zA-Z0-9_]+)$', views.chrRoomDelete , name='chrRoomDelete'),



    url(r'^mess_opi/$', views.mess_opi,name='mess_opi'),
    url(r'^mess_opi/calculate$', views.opi_calculate,name='opi_calculate'),
    url(r'^mess_automation/$', views.mess_automation,name='mess_automation'),
    url(r'^mess_import_export_files/$',views.import_export_files,name='mess_import_export'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
