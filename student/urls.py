from django.urls import path
from . import views

urlpatterns = [
    path('<build_id>/', views.in_out, name='in_out'),
]
