from django.urls import path
from  . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.Logout, name='Logout'),
    path('query/', views.query, name='query'),
    path('', views.in_out_list, name='in_out_list'),
    path('<flag>', views.export, name='export'),
    path('count/', views.count, name='count'),
]