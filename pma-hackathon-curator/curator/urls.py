"""curator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/personas', views.get_personas),
    path('api/reactions', views.get_reactions),
    path('api/galleries', views.get_galleries),
    path('api/gallery/<int:gallery_id>/activity', views.get_gallery_activity),
    path('api/gallery/<int:gallery_id>/recommendation', views.get_gallery_recommendation),
    path('api/reaction', views.add_reaction),
    path('api/visitor', views.add_visitor),
    path('recommendation/<int:artwork_id>', views.recommendations_for_artwork),
    path('admin/', admin.site.urls),
]
