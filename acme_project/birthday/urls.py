from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    path('list/', views.birthday_list, name='list'),
    path('list_cbw/', views.BirthdayListView.as_view(), name='list_cbw'),
    path('<int:pk>/edit/', views.birthday, name='edit'),
    path('<int:pk>/delete/', views.delete_birthday, name='delete'),
]
