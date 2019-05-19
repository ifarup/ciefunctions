from django.urls import path, re_path
from web import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path('get_plot/(?P<plot>\w+)/(?P<grid>\d+)/(?P<cie31>\d+)/(?P<cie64>\d+)/(?P<labels>\d+)/(?P<norm>\d+)/(?P<log10>\d+)', views.get_plot, name='get_plot'),
    re_path('get_csv/(?P<plot>\w+)', views.get_csv, name="get_csv"),
    re_path('get_table/(?P<plot>\w+)/(?P<norm>\d+)/(?P<log10>\d+)', views.get_table, name="get_table"),
    re_path('get_description/(?P<plot>\w+)/(?P<norm>\d+)/(?P<log10>\d+)', views.get_description, name="get_description"),
    re_path('compute/(?P<field_size>[\d.]+)/(?P<age>[\d.]+)/(?P<lambda_min>[\d.]+)/(?P<lambda_max>[\d.]+)/(?P<lambda_step>[\d.]+)', views.compute, name="compute"),
]
