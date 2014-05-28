# Create your views here.
from __future__ import absolute_import
import tc182 as tc
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
	context = {}
	
	try:

		last_field =  float(request.POST["last_field"])
		last_age = int(request.POST["last_age"])
		last_resolution =  float(request.POST["last_resolution"])

		print [last_field, last_age, last_resolution]

		tc_obj = get_tc(last_field, last_age, last_resolution)
		
		print tc_obj
		
		context = { 'tc_obj' : tc_obj }

		print tc_obj.purple_line_cc64
	
		return render(request, 'web/index.html', context)
	
	except: 
	
		print "No data received, or malformed"
		
		return render(request, 'web/index.html', context)

def get_tc(last_field=7, last_age=30, last_resolution=1):

	tc_obj = tc.compute_tabulated(last_field, last_age, last_resolution)
	return tc_obj
	
def plot_test1(request):

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

	field_size = 2.0;
	age = 32;
	lambda_min = 390.0;
	lambda_max = 830.0;
	lambda_step = 1.0;
	

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

		
	tab, plot_data = compute( field_size, age, lambda_min, lambda_max, lambda_step )
	
	tab_str = tab["lms_standard"].tolist()
	
	for j in range(1,4):
		for i in range(len(tab_str)):
			tab_str[i][j] = "%.6e" % tab_str[i][j]

	
	html_str = ''


	context = { 'tab_str' : tab_str,
				'xyzFig' : mark_safe(draw_plot(plot_data["lms"])),
				'html_str' : html_str,
	}
		
	return render(request, 'web/plot.html', context)
	

def compute( field_size, age, lambda_min, lambda_max, lambda_step ):

	tab, plot = tc.compute_tabulated( field_size, age, lambda_min, lambda_max, lambda_step )

	return tab, plot


@shared_task
def draw_plot( plot_data ):

	mpl.rcParams['lines.linewidth'] = 1
	
	fig, axes = plt.subplots()
	axes.plot(plot_data[:,0], plot_data[:,1], 'r')
	axes.plot(plot_data[:,0], plot_data[:,2], 'g')
	axes.plot(plot_data[:,0], plot_data[:,3], 'b')
	axes.axis([350, 850, -.05, 1.05])
	
	axes.set_title("The Plot!", size=14)
	axes.grid(color='lightgray', alpha=0.8)

	return mpld3.fig_to_html(fig, template_type='general')


	
	
	
	
	
	
	
	
