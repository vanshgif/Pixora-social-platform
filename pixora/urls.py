from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Pixora 🚀</h1>")

urlpatterns = [
    path("", home, name="home"),  # root path
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
]
