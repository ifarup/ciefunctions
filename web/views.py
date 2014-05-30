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
import matplotlib.pyplot as plt, mpld3
from django.utils.safestring import mark_safe
from celery import shared_task
from numpy import *
	
def home(request):

#	Returns
#    -------
#    xyz : ndarray
#       	The computed colour matching functions.
#    cc : ndarray
#        The chromaticity coordinates.
#    cc_white : ndarray
#        The chromaticity coordinates for equi-energy stimulus.
#    mat : ndarray
#        The 3x3 matrix for converting from LMS to XYZ.
#    lms_standard : ndarray
#        The computed LMS functions at the given standard resolution.
#    lms_base : ndarray
#        The computed LMS functions at full available resolution (9 sign. fig.).        
#    bm : ndarray
#        The computed Boynton-MacLeod chromaticity coordinates.
#    bm_white : ndarray
#        The Boynton-MacLeod coordinates for equi-energy stimulus.
#    lm : ndarray
#        The computed normalised lm coordinates.
#    lm_white : ndarray
#        The lm coordinates for equi-energy stimulus.
#    lambda_test_min : int
#        The wavelength of minimum x chromaticity value.
#    purple_line_cc : ndarray
#        Chromaticity coordinates for the endpoints of the purple line.
#    purple_line_bm : ndarray
#        Boynton-MacLeod coordinates for the endpoints of the purple line.
#    purple_line_lm : ndarray
#        lm coordinates for the endpoints of the purple line.
#    plots : dict
#        Versions of xyz, cc, lms, bm, lm at 0.1 nm for plotting. Includes also CIE1964 and CIE1931 data. 

	#field_size = 2.0;
	#age = 32;
	#lambda_min = 390.0;
	#lambda_max = 830.0;
	#lambda_step = 1.0;

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
	fig_list = []  #List containing all the figures/plots
	tab_list = []  #List containing all the tabulated data
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	results, plots = tc182.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)	
	options = { 'grid' : True,
            	'cie31' : True,
            	'cie64' : False,
            	'labels' : True }
    #0 #xyz 
	
	tc182.plot.xyz(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.xyz(results,'XYZ'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	theTable = mark_safe(tc182.table.xyz(results));
	tab_list.append(theTable)
	
    #1 #xy
    
	tc182.plot.xy(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.xy(results,'XY'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)

	theTable = mark_safe(tc182.table.xy(results));
	tab_list.append(theTable)

	
	#2 #lms
    
	tc182.plot.lms(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.lms(results,'LMS'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	theTable = mark_safe(tc182.table.lms(results));
	tab_list.append(theTable)

	
	#3 #lms_base
    
	tc182.plot.lms_base(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.lms_base(results,'LMS BASE'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	theTable = mark_safe(tc182.table.lms_base(results));
	tab_list.append(theTable)

	#4 #bm
	
	tc182.plot.bm(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.bm(results,'BM'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	theTable = mark_safe(tc182.table.bm(results));
	tab_list.append(theTable)

	#5 #lm
	
	tc182.plot.lm(ax, plots, options)
	
	theDescription = mark_safe(tc182.description.lm(results,'LM'))
	html_list.append(theDescription)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	theTable = mark_safe(tc182.table.lm(results));
	tab_list.append(theTable)
	
	# #6 #xyz31
# 	
# 	tc182.plot.xyz31(ax, plots, options)
# 	
# 	theDescription = mark_safe(tc182.description.xyz31(results,'XYZ31'))
# 	html_list.append(theDescription)
# 	
# 	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
# 	fig_list.append(theFig)
# 	
# 	theTable = mark_safe(tc182.table.xyz31(results));
# 	tab_list.append(theTable)
# 	
# 	#7 #xyz64
# 
# 	tc182.plot.xyz64(ax, plots, options)
# 	
# 	theDescription = mark_safe(tc182.description.xyz64(results,'XYZ64'))
# 	html_list.append(theDescription)
# 	
# 	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
# 	fig_list.append(theFig)
# 	
# 	theTable = mark_safe(tc182.table.xyz64(results));
# 	tab_list.append(theTable)
# 
# 	
# 	#8 #xy31
# 	
# 	tc182.plot.xy31(ax, plots, options)
# 	
# 	theDescription = mark_safe(tc182.description.xy31(results,'XY31'))
# 	html_list.append(theDescription)
# 	
# 	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
# 	fig_list.append(theFig)
# 	
# 	theTable = mark_safe(tc182.table.xy31(results));
# 	tab_list.append(theTable)
# 
# 	
# 	#9 #xy64
# 	tc182.plot.xy64(ax, plots, options)
# 	
# 	theDescription = mark_safe(tc182.description.xy64(results,'XY64'))
# 	html_list.append(theDescription)
# 	
# 	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
# 	fig_list.append(theFig)
# 	
# 	theTable = mark_safe(tc182.table.xy64(results));
# 	tab_list.append(theTable)


	context = { 'tab_list' : tab_list,
				'fig_list' : fig_list,
				'html_list' : html_list,
				'field_size' : field_size,
				'age'	: age,
				'lambda_min' : lambda_min,
				'lambda_max' : lambda_max,
				'lambda_step'	: lambda_step,
	}


	return render(request, 'web/plot.html', context)