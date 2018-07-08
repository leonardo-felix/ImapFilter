from django.conf.urls import include
from django.urls import path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imapfilter/', include('imapfilter.urls'))
]
