from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from web import views

#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
        url(r'^$', views.home, name='home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^get_plot/(?P<plot>\w+)/(?P<grid>\d+)/(?P<cie31>\d+)/(?P<cie64>\d+)/(?P<labels>\d+)/(?P<norm>\d+)', views.get_plot, name='get_plot'),
    url(r'^get_csv/(?P<plot>\w+)', views.get_csv, name="get_csv"),
    url(r'^get_table/(?P<plot>\w+)/(?P<norm>\d+)', views.get_table, name="get_table"),
    url(r'^get_description/(?P<plot>\w+)/(?P<norm>\d+)', views.get_description, name="get_description"),
    url(r'^compute/(?P<field_size>[\d.]+)/(?P<age>[\d.]+)/(?P<lambda_min>[\d.]+)/(?P<lambda_max>[\d.]+)/(?P<lambda_step>[\d.]+)/', views.compute, name="compute"),
)
