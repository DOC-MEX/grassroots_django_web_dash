from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    # ex: /fieldtrial/
    path('', views.index_loading, name='index'),
    path('all', views.index, name='index_real'),
    path('study/<study_id>', views.single_study),
    path('plots/<plot_id>', views.single_plot),

    path('ajax/get_fieldtrial/', views.search_fieldtrial),
    re_path(r'(?P<fieldtrial_id>[A-z0-9-\w%]+)$', views.single_fieldtrial)


]