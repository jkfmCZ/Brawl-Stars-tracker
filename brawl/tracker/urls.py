from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^p/(?P<tag>#[0-9A-Z]{9})/$', views.p_report, name='player_report'),
]
