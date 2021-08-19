"""Video_Fetch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


#from background_task.models import Task
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import  url
from fetch_api import background_processes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('fetch_api.urls')),
]

REPEAT_PROCESS = 100000000
def start_process(repeat):
    try:
        Task.objects.all().delete()
    except:
        pass
    background_processes.schelude_jobs()


#start_process(REPEAT_PROCESS)
