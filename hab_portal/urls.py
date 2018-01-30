"""hab_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from hab_app import views
from django.conf.urls.static import static
from . import settings
urlpatterns = [
    url(r'^hab_portal/home/$', views.home,name='home'),
    url(r'^hab_portal/admin/', admin.site.urls),
    url(r'^hab_portal/hab_app/', include('hab_app.urls')),
    url(r'^hab_portal/student_portal/', include('student_portal.urls')),
    url(r'^hab_portal/logout1/$', views.logout1,name='logout1'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
