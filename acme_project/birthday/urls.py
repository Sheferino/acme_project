from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    path('birthday_cbv/', views.BirthdayCreateView.as_view(), name='create_cbv'),
    path('list/', views.birthday_list, name='list'),
    path('list_cbv/', views.BirthdayListView.as_view(), name='list_cbv'),
    path('<int:pk>/edit/', views.birthday, name='edit'),
    path('<int:pk>/edit_cbv/', views.BirthdayUpdateView.as_view(), name='edit_cbv'),
    path('<int:pk>/delete/', views.delete_birthday, name='delete'),
    path('<int:pk>/delete_cbv/', views.BirthdayDeleteView.as_view(), name='delete_cbv'),
]
