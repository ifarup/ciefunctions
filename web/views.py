# Create your views here.
from __future__ import absolute_import
import tc182 as tc # the base package, includes the computational part
import tc182.plot # if you want to do the plots as well
import tc182.description # if you want to generate the html descriptions
import tc182.table # For the tables

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from mpld3 import plugins
import matplotlib as mpl
mpl.use("AGG")
import matplotlib.pyplot as plt
import mpld3
from django.utils.safestring import mark_safe
from celery import shared_task
from numpy import *

def get_plot(request, plot, grid, cie31, cie64, labels):
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plots = request.session['plots']
	results = request.session['results']
	
	options = { 'grid' 			: int(grid),
				'full_title'	: False,
            	'cie31' 		: int(cie31),
            	'cie64' 		: int(cie64),
            	'labels' 		: int(labels),
            	'axis_labels'	: False,
            	'label_fontsize' : 12 }
            	
	if (plot == 'xyz'):
		tc182.plot.xyz(ax, plots, options)
		
	elif (plot == 'xy'):
		tc182.plot.xy(ax, plots, options)
	
	elif (plot == 'lms'):
		tc182.plot.lms(ax, plots, options)
	
	elif (plot == 'lms_base'):
		tc182.plot.lms_base(ax, plots, options)
	
	elif (plot == 'bm'):
		tc182.plot.bm(ax, plots, options)
	
	elif (plot == 'lm'):
		tc182.plot.lm(ax, plots, options)
		
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	resulting_plot = theFig;
	plt.close(fig)
	return HttpResponse(resulting_plot);


def home(request):

	try:
		field_size = float(request.POST["field_size"])
		print "field_size: %s " % field_size
	except:
		field_size = 2.0
		print "field_size: %s " % field_size
		
	try:
		age = int(request.POST["age"])
		print "age: %s" % age
	except:
		age = 32
		print "age: %s" % age
	
	try:
		lambda_min = int(request.POST["lambda_min"])
		print "lambda_min: %s" % lambda_min
	except:
		lambda_min = 390.0
		print "lambda_min: %s" % lambda_min
	
	try:
		lambda_max = int(request.POST["lambda_max"])
		print "lambda_max: %s" % lambda_max
	except:
		lambda_max = 830.0
		print "lambda_max: %s" % lambda_max
	
	try:
		lambda_step = int(request.POST["lambda_step"])
		print "lambda_step: %s" % lambda_step
	except:
		lambda_step = 1.0
		print "lambda_step: %s" % lambda_step
		
	html_list = [] #List containing all the theDescriptions
	tab_list = []  #List containing all the tabulated data
	
	results, plots = tc182.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
	
	request.session['results'] = results
	request.session['plots'] = plots
	
    #0 #xyz 
	
	theDescription = mark_safe(tc182.description.xyz(results,'XYZ'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xyz(results));
	tab_list.append(theTable)
	
    #1 #xy
	
	theDescription = mark_safe(tc182.description.xy(results,'XY'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xy(results));
	tab_list.append(theTable)

	
	#2 #lms
	
	theDescription = mark_safe(tc182.description.lms(results,'LMS'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lms(results));
	tab_list.append(theTable)

	
	#3 #lms_base
    
	theDescription = mark_safe(tc182.description.lms_base(results,'LMS BASE'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lms_base(results));
	tab_list.append(theTable)

	#4 #bm
	
	theDescription = mark_safe(tc182.description.bm(results,'BM'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.bm(results));
	tab_list.append(theTable)

	#5 #lm
	
	theDescription = mark_safe(tc182.description.lm(results,'LM'))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lm(results));
	tab_list.append(theTable)
	



	context = { 'tab_list' : tab_list,
				'html_list' : html_list,
				'field_size' : field_size,
				'age'	: age,
				'lambda_min' : lambda_min,
				'lambda_max' : lambda_max,
				'lambda_step'	: lambda_step,
	}


	return render(request, 'web/plot.html', context)