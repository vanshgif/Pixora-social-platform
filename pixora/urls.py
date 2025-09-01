from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from  django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("<h1>Welcome to Pixora 🚀</h1>")

urlpatterns = [
    path("", home, name="home"),  # root path
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("posts.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)