from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from backend.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
