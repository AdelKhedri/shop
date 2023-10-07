
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('oq39r71t!7i6i67w@2fbh4&iyi76*23r(8o7834t-)ry521_trh79a+gre67-wef=12ew[w233]2ew3{23eq;234WFEW2>234<23Q,/', admin.site.urls),
    path('', include('members.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
