from django.contrib import admin
from web.models import Result, Plot

class ResultAdmin(admin.ModelAdmin):
	list_display = ('field_size','age', 'lambda_min', 'lambda_max', 'lambda_step')

class PlotAdmin(admin.ModelAdmin):
	list_display = ('field_size','age', 'lambda_min', 'lambda_max', 'lambda_step')



# Register your models here.

admin.site.register(Result)
admin.site.register(Plot)