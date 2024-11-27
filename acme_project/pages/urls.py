from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('old/', views.homepage, name='homepage_old'),
]
