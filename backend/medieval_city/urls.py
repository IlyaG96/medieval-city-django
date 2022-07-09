from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('city/', views.show_city, name='show_city'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('civilian/<int:civilian_id>/', views.view_civilian, name='civilian'),

]


