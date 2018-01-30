from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    url(r'login/$', views.manual_login, name='login'),
    # url(r'home/$', views.HomeView.as_view(), name='home'),
    url(r'logout/$', views.manual_logout, name='logout'),
    url(r'messfeedback/$', login_required(views.check_filled_feedback), name='feedback'),
    url(r'messfeedback/new$', login_required(views.NewFeedback.as_view()), name='new_feedback'),
    url(r'messfeedback/update$', login_required(views.UpdateFeedback.as_view()), name='update_feedback'),
    url(r'preference/$', login_required(views.check_filled_preference), name='preference'),
    url(r'preference/new$', login_required(views.NewPreference.as_view()), name='new_preference'),
    url(r'preference/update$', login_required(views.UpdatePreference.as_view()), name='update_preference'),
    url(r'updateinfo$', login_required(views.updateinfo), name='updateinfo'),
    url(r'track$', views.track, name='track'),
    url(r'gensecfeedback$', login_required(views.gensec_feedback), name='gensecfeedback'),
    url(r'gensecinfo$', login_required(views.gensec_info), name='gensecinfo'),

]
