"""cars URL Configuration

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
from django.urls import path
from .views import index, render_add_template, CreateCarView, RateCarView, PopularCarsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('add/', render_add_template, name='add'),
    path('cars/', CreateCarView.as_view(), name='cars'),
    path('rate/', RateCarView.as_view(), name='rate'),
    path('popular/', PopularCarsView.as_view(), name='populars')
]
