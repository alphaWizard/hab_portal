from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'login/$', views.manual_login, name='login'),
    # url(r'home/$', views.HomeView.as_view(), name='home'),
    url(r'logout/$', views.manual_logout, name='logout'),
    url(r'messfeedback/$', views.check_filled_feedback, name='feedback'),
    url(r'messfeedback/new$', views.NewFeedback.as_view(), name='new_feedback'),
    url(r'messfeedback/update$', views.UpdateFeedback.as_view(), name='update_feedback'),
    url(r'preference/$', views.check_filled_preference, name='preference'),
    url(r'preference/new$', views.NewPreference.as_view(), name='new_preference'),
    url(r'updateinfo$', views.updateinfo, name='updateinfo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
