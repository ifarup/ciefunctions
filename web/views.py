# Create your views here.
from __future__ import absolute_import
import tc1_97 as tc # the base package, includes the computational part
import tc1_97.plot # if you want to do the plots as well
import tc1_97.description # if you want to generate the html descriptions
import tc1_97.table # For the tables

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from mpld3 import plugins
import matplotlib as mpl
mpl.use("AGG")
import matplotlib.pyplot as plt
import mpld3
from django.utils.safestring import mark_safe

import numpy as np
from io import StringIO

from web.models import Result, Plot
from django.shortcuts import get_object_or_404

import codecs
#import json
from json_tricks import dump, dumps, load, loads, strip_comments



import logging
log = logging.getLogger(__name__)

import time
from time import gmtime, strftime
import timeit

#Global options for plot, table & description. Contains defaults.

options = { 	'grid' 			: 0,
				'full_title'	: False,
            	'cie31' 		: 0,
            	'cie64' 		: 0,
            	'labels' 		: 0,
            	'axis_labels'	: False,
            	'label_fontsize' : 12,
            	'norm'			: False,
            	'title_fontsize' : 13
}

def updateOptions(optionSet):

	try: options['grid'] = optionSet['grid']
	except: pass
	
	try: options['full_title'] = optionSet['full_title']
	except: pass
	
	try: options['cie31'] = optionSet['cie31']
	except: pass
	
	try: options['cie64'] = optionSet['cie64']
	except: pass
	
	try: options['labels'] = optionSet['labels']
	except: pass
	
	try: options['axis_labels'] = optionSet['axis_labels']
	except: pass
	
	try: options['label_fontsize'] = optionSet['label_fontsize']
	except: pass
	
	try: options['norm'] = bool(optionSet['norm'])
	except: pass

	return

def time_now():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
def get_filename_params(request):
	
	results	 		= request.session['results']
	
	age 			= str(int(results['age']))
	field_size 		= str(results['field_size'].replace(".", "_"))
	lambda_min 		= str(results['lambda_min'].replace(".", "_"))
	lambda_max 		= str(results['lambda_max'].replace(".", "_"))
	lambda_step 	= str(results['lambda_step'].replace(".","_"))
	
	filename_params = 	"___fs" +  field_size + "___age" + age + "___range" + lambda_min + "__" + lambda_max + "___step" + lambda_step

	return filename_params

def get_plot(request, plot, grid, cie31, cie64, labels, norm):
	start = time.time()
	log.debug("[%s] Requesting %s/%s/%s/%s/%s/%s - \t\tsID: %s" % (time_now(), plot, grid, cie31, cie64, labels, norm, request.session.session_key))

	#Figure
	fig = plt.figure()

	#Figure size, in inches, 100 dots-per-inch
	dpi = 80
	fig.set_size_inches(8.0, 4.8)
	ax = fig.add_subplot(111)
	plots = request.session['plots']
	results = request.session['results']
	
	optionSet = { 	'grid' 				: int(grid),
            		'cie31' 			: int(cie31),
            		'cie64' 			: int(cie64),
            		'labels' 			: int(labels),
            		'norm'				: bool(int(norm)),   	
    }
    
	updateOptions(optionSet)
    
	if (plot == 'xyz'):
		tc1_97.plot.xyz(ax, plots, options)
		
	elif (plot == 'xy'):
		tc1_97.plot.xy(ax, plots, options)
	
	elif (plot == 'lms'):
		tc1_97.plot.lms(ax, plots, options)
	
	elif (plot == 'lms_base'):
		tc1_97.plot.lms_base(ax, plots, options)
	
	elif (plot == 'bm'):
		tc1_97.plot.bm(ax, plots, options)
	
	elif (plot == 'lm'):
		tc1_97.plot.lm(ax, plots, options)
	
	elif (plot == 'xyz31'):
		tc1_97.plot.xyz31(ax, plots, options)

	elif (plot == 'xyz64'):
		tc1_97.plot.xyz64(ax, plots, options)
	
	elif (plot == 'xy31'):
		tc1_97.plot.xy31(ax, plots, options)

	elif (plot == 'xy64'):
		tc1_97.plot.xy64(ax, plots, options)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	resulting_plot = theFig;
	plt.close(fig)
	stop = time.time()
	log.debug("[%s] Plot %s/%s/%s/%s/%s produced in %s seconds - \t\tsID: %s" % ( time_now(), plot,  grid, cie31, cie64, labels, str(stop - start), request.session.session_key))
	return HttpResponse(resulting_plot);

def get_table(request, plot, norm):
	results = request.session['results']

	optionSet = {		'norm'				: bool(int(norm))}
    
	updateOptions(optionSet)
	
	if (plot == 'xyz'):
		return HttpResponse(mark_safe(tc1_97.table.xyz(results, options, '')))

	elif (plot == 'xy'):
		return HttpResponse(mark_safe(tc1_97.table.xy(results, options, '')))
	
	elif (plot == 'lms'):
		return HttpResponse(mark_safe(tc1_97.table.lms(results, options, '')))
	
	elif (plot == 'lms_base'):
		return HttpResponse(mark_safe(tc1_97.table.lms_base(results, options, '')))
	
	elif (plot == 'bm'):
		return HttpResponse(mark_safe(tc1_97.table.bm(results, options, '')))
	
	elif (plot == 'lm'):
		return HttpResponse(mark_safe(tc1_97.table.lm(results, options, '')))
	
	elif (plot == 'xyz31'):
		return HttpResponse(mark_safe(tc1_97.table.xyz31(results, options, '')))
	
	elif (plot == 'xyz64'):
		return HttpResponse(mark_safe(tc1_97.table.xyz64(results, options, '')))
		
	elif (plot == 'xy31'):
		return HttpResponse(mark_safe(tc1_97.table.xy31(results, options, '')))

	elif (plot == 'xy64'):
		return HttpResponse(mark_safe(tc1_97.table.xy64(results, options, '')))
		
	else:
		return HttpResponse('No description for plot %s' % plot)

	return HttpResponse('Table %s' % plot)
	

def get_description(request, plot, norm):
	results = request.session['results']
	
	optionSet = {		'norm'				: bool(int(norm))}
    
	updateOptions(optionSet)

	if (plot == 'xyz'):
		return HttpResponse(mark_safe(tc1_97.description.xyz(results, '', options, '')))

	elif (plot == 'xy'):
		return HttpResponse(mark_safe(tc1_97.description.xy(results, '', options, '')))
	
	elif (plot == 'lms'):
		return HttpResponse(mark_safe(tc1_97.description.lms(results, '', options, '')))
	
	elif (plot == 'lms_base'):
		return HttpResponse(mark_safe(tc1_97.description.lms_base(results, '', options, '')))
	
	elif (plot == 'bm'):
		return HttpResponse(mark_safe(tc1_97.description.bm(results, '', options, '')))
	
	elif (plot == 'lm'):
		return HttpResponse(mark_safe(tc1_97.description.lm(results, '', options, '')))
	
	elif (plot == 'xyz31'):
		return HttpResponse(mark_safe(tc1_97.description.xyz31(results, '', options, '')))
	
	elif (plot == 'xyz64'):
		return HttpResponse(mark_safe(tc1_97.description.xyz64(results, '', options, '')))
		
	elif (plot == 'xy31'):
		return HttpResponse(mark_safe(tc1_97.description.xy31(results, '', options, '')))
		return HttpResponse(mark_safe(tc1_97.description.xy31(results, '', options, '')))

	elif (plot == 'xy64'):
		return HttpResponse(mark_safe(tc1_97.description.xy64(results, '', options, '')))
		
	else:
		return HttpResponse('No description for plot %s' % plot)

def get_csv(request, plot):

	format = { 	'xyz' 			:  '%.1f, %.6e, %.6e, %.6e',
				'xyz31' 		:  '%.1f, %.6e, %.6e, %.6e',
				'xyz64' 		:  '%.1f, %.6e, %.6e, %.6e',
				'xy'			: '%.1f, %.5f, %.5f, %.5f',
				'xy31'			: '%.1f, %.5f, %.5f, %.5f',
				'xy64'			: '%.1f, %.5f, %.5f, %.5f',
			   	'lms' 			: '%.1f, %.5e, %.5e, %.5e',
			   	'lms_base'		: '%.1f, %.8e, %.8e, %.8e',
			   	'bm'			: '%.1f, %.6f, %.6f, %.6f',
			   	'lm'			: '%.1f, %.6f, %.6f, %.6f',
			   	'cc'			: '%.1f, %.5f, %.5f, %.5f'
	}

	plot_name = {	'xyz' 			: 'xyz',
					'xyz31' 		: 'xyz31',
					'xyz64' 		: 'xyz64',
					'xy'			: 'xy',
					'xy31'			: 'xy31',
					'xy64'			: 'xy64',
			   		'lms' 			: 'lms',
			   		'lms_base'		: 'lms_9figs',
			   		'bm'			: 'ls_mb',
			   		'lm'			: 'lm',
			   		'cc'			: 'cc'
	}

	filename = plot_name[plot] + get_filename_params(request) + ".csv"
	
	output = StringIO.StringIO()
	thePlot = request.session['results']
	np.savetxt(output, thePlot[plot], format[plot])
	response = HttpResponse(output.getvalue(), mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename = "%s"' % filename
	return response
	
def compute(request, field_size, age, lambda_min, lambda_max, lambda_step):
# The values here are sanitized on the client side, so we can trust them.
	start 		= 	time.time()
	field_size 	= 	float(field_size)
	age			= 	float(age)
	lambda_min	=	float(lambda_min)
	lambda_max	=	float(lambda_max)
	lambda_step	=	float(lambda_step)
	
#	try:
#		serialized_test_results = Result.objects.get(field_size=field_size, age=age, lambda_min=lambda_min, lambda_max=lambda_max, lambda_step=lambda_step)
#		test_results = json.loads(serialized_test_results.tolist())
#		request.session['results'] = test_results.get_data().tolist()
#		results = test_results.get_data().tolist()
#	
#		serialized_test_plots = Plot.objects.get(field_size=field_size, age=age, lambda_min=lambda_min, lambda_max=lambda_max, lambda_step=lambda_step)
#		test_plot = serializers.loads(serialized_test_plots.tolist())
#		request.session['plots'] = test_plots.get_data().tolist()
#		plots = test_plots.get_data().tolist()
#		
#	except Exception as e:
#		print("1st try %s") % e
#		print("Computing ...")
#		log.debug("[%s] Computing -> Age: %s, f_size: %s, l_min: %s, l_max: %s, l_step: %s, sID: %s"
#				% ( time_now(), age, field_size, lambda_min, lambda_max, lambda_step, request.session.session_key))
#		results, plots = tc1_97.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
#		request.session['results'] = results
#		request.session['plots'] = plots
#		
#		try:
#			#serialized_results = json.dumps(results.tolist())
#            serialized_results = json.dumps("")
#			#new_result = Result( 	field_size=field_size, 
#			#						age=age, 
#			#						lambda_min=lambda_min, 
#			#						lambda_max=lambda_max, 
#			#						lambda_step=lambda_step, 
#			#						data=serialized_results )
#			#new_result.save()
#		except Exception as e:
#			print("Can't serialize results: %s") % e
#			
#		try:
#			serialized_plots = json.dumps(plots.tolist())
#			#new_plot = Plot ( 	field_size=field_size,
#			#					age=age, 
#			#					lambda_min=lambda_min, 
#			#					lambda_max=lambda_max, 
#			#					lambda_step=lambda_step, 
#			#					data=plots )
#			#new_plot.save()
#		except Exception as e:
#			#print "Can't serialize plots: %s" % e
#			print(e)
			
	stop = time.time()
	log.debug("[%s] Compute performed in %s seconds - sID: %s" % ( time_now(), str(stop - start), request.session.session_key))
	
	return HttpResponse('Calculate fields updated')

def home(request):

	log.info("[%s] New request. sessionId: %s" % (time_now(), request.session.session_key))
	log.info("[%s] User Agent: %s" % (time_now(), request.META['HTTP_USER_AGENT']))
	#log.info("[%s] Remote Host (ip): %s (%s)" % (time_now(), request.META['REMOTE_HOST'], request.META['REMOTE_ADDR']))

	try:
		field_size = float(request.POST["field_size"])
		
	except:
		field_size = 2.0
		
	try:
		age = int(request.POST["age"])
		
	except:
		age = 32
		
	
	try:
		lambda_min = float(request.POST["lambda_min"])
		
	except:
		lambda_min = 390.0
		
	try:
		lambda_max = float(request.POST["lambda_max"])
		
	except:
		lambda_max = 830.0
		
	
	try:
		lambda_step = float(request.POST["lambda_step"])
		
	except:
		lambda_step = 1.0
		
	
	log.debug("[%s] Age: %s, f_size: %s, l_min: %s, l_max: %s, l_step: %s - sID: %s"
				% ( time_now(), age, field_size, lambda_min, lambda_max, lambda_step, request.session.session_key))

	#Call an initial compute
	start = time.time()
	request.session['results'], request.session['plots'] = tc1_97.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
	stop = time.time()
	log.debug("[%s] Initial compute performed in %s seconds - \tsID: %s" % ( time_now(), str(stop - start), request.session.session_key))
	
	context = { 
				'field_size' : field_size,
				'age'	: age,
				'lambda_min' : lambda_min,
				'lambda_max' : lambda_max,
				'lambda_step'	: lambda_step,
	}


	return render(request, 'web/plot.html', context)
