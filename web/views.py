# Create your views here.
from __future__ import absolute_import
import tc182 as tc # the base package, includes the computational part
import tc182.plot # if you want to do the plots as well
import tc182.html # if you want to generate the html descriptions

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
		
	html_list = [] #List containing all the html_strings
	fig_list = []  #List containing all the figures/plots
	tab_list = []  #List containing all the tabulated data
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	results, plots = tc182.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)	
	options = { 'grid' : True,
            	'cie31' : True,
            	'cie64' : False,
            	'labels' : True }
    #xyz
	
	tc182.plot.xyz(ax, plots, options)
	
	html_string = mark_safe(tc182.html.xyz(results,'Heading'))
	html_list.append(html_string)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
    #xy
    
	tc182.plot.xy(ax, plots, options)
	
	html_string = mark_safe(tc182.html.xy(results,'Heading'))
	html_list.append(html_string)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	#lms
    
	tc182.plot.lms(ax, plots, options)
	
	html_string = mark_safe(tc182.html.lms(results,'Heading'))
	html_list.append(html_string)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	#lms_base
    
	tc182.plot.lms_base(ax, plots, options)
	
	html_string = mark_safe(tc182.html.lms_base(results,'Heading'))
	html_list.append(html_string)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	#bm
	
	tc182.plot.bm(ax, plots, options)
	
	html_string = mark_safe(tc182.html.bm(results,'Heading'))
	html_list.append(html_string)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	fig_list.append(theFig)
	
	
	
	### TABULATED DATA ###
	
	#tab_str = tab["lms_standard"].tolist()
	
	#for j in range(1,4):
	#	for i in range(len(tab_str)):
	#		tab_str[i][j] = "%.6e" % tab_str[i][j]


	context = { #'tab_str' : tab_str,
				'fig_list' : fig_list,
				'html_list' : html_list,
				'field_size' : field_size,
				'age'	: age,
				'lambda_min' : lambda_min,
				'lambda_max' : lambda_max,
				'lambda_step'	: lambda_step,
	}
		
	
	return render(request, 'web/plot.html', context)	
	
	
	
