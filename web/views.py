# Create your views here.
from __future__ import absolute_import

# Web API
import webapi.plot
import webapi.description
import webapi.table
import webapi.utils
import webapi.compute


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import matplotlib as mpl
mpl.use("AGG")
import matplotlib.pyplot as plt
import mpld3
from django.utils.safestring import mark_safe

import numpy as np
from io import StringIO

import logging
log = logging.getLogger(__name__)

import time
from time import gmtime, strftime

#Global options for plot, table & description. Contains defaults.

options = { 	'grid' 			 : 0,
				'full_title'	 : True,
            	'cie31' 		 : 0,
            	'cie64' 		 : 0,
            	'labels' 		 : 0,
            	'axis_labels'	 : False,
            	'label_fontsize' : 12,
            	'norm'			 : False,
            	'title_fontsize' : 13,
			    'log10'          : False
}

def updateOptions(optionSet):

	try: options['grid'] = optionSet['grid']
	except: pass
	
	try: options['full_title'] = bool(optionSet['full_title'])
	except: pass
	
	try: options['cie31'] = optionSet['cie31']
	except: pass
	
	try: options['cie64'] = optionSet['cie64']
	except: pass
	
	try: options['labels'] = optionSet['labels']
	except: pass
	
	try: options['axis_labels'] = bool(optionSet['axis_labels'])
	except: pass
	
	try: options['label_fontsize'] = optionSet['label_fontsize']
	except: pass
	
	try: options['norm'] = bool(optionSet['norm'])
	except: pass

	try: options['log10'] = bool(optionSet['log10'])
	except: pass

	return

def time_now():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
def get_filename_params(request):
	
	results	 		= request.session['results']
	
	age 			= str(int(results['age']))
	field_size 		= str(results['field_size'].replace(".", "_"))
	lambda_min 		= str(results['λ_min'].replace(".", "_"))
	lambda_max 		= str(results['λ_max'].replace(".", "_"))
	lambda_step 	= str(results['λ_step'].replace(".","_"))
	
	filename_params = 	"___fs" +  field_size + "___age" + age + "___range" + lambda_min + "__" + lambda_max + "___step" + lambda_step

	return filename_params

def get_plot(request, plot, grid, cie31, cie64, labels, norm, log10):
	start = time.time()
	log.debug("[%s] Requesting %s/%s/%s/%s/%s/%s/%s - \t\tsID: %s" % (time_now(), plot, grid, cie31, cie64, labels, norm, log10, request.session.session_key))

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
					'log10'				: bool(int(log10))
    }
    
	updateOptions(optionSet)

	if plot == 'lms':
		webapi.plot.lms(ax, plots, options)
	
	elif plot == 'lms_base':
		webapi.plot.lms_base(ax, plots, options)
	
	elif plot == 'bm':
		webapi.plot.bm(ax, plots, options)
	
	elif plot == 'lm':
		webapi.plot.lm(ax, plots, options)

	elif plot == 'xyz':
		webapi.plot.xyz(ax, plots, options)
	
	elif plot == 'xy':
		webapi.plot.xy(ax, plots, options)

	elif plot == 'xyz_purples':
		webapi.plot.xyz_purples(ax, plots, options)

	elif plot == 'xy_purples':
		webapi.plot.xy_purples(ax, plots, options)

	elif plot == 'xyz31':
		webapi.plot.xyz31(ax, plots, options)

	elif plot == 'xyz64':
		webapi.plot.xyz64(ax, plots, options)
	
	elif plot == 'xy31':
		webapi.plot.xy31(ax, plots, options)

	elif plot == 'xy64':
		webapi.plot.xy64(ax, plots, options)

	htmlFig = mpld3.fig_to_html(fig, template_type='general')
	theFig = mark_safe(htmlFig)
	resulting_plot = theFig
	plt.close(fig)
	stop = time.time()
	log.debug("[%s] Plot %s/%s/%s/%s/%s/%s/%s produced in %s seconds - \t\tsID: %s" % ( time_now(), plot,  grid, cie31, cie64, labels, norm, log10, str(stop - start), request.session.session_key))
	print("[%s] Plot %s/%s/%s/%s/%s/%s/%s produced in %s seconds - \t\tsID: %s" % ( time_now(), plot,  grid, cie31, cie64, labels, norm, log10, str(stop - start), request.session.session_key))
	return HttpResponse(resulting_plot)

def get_table(request, plot, norm, log10):
	results = request.session['results']

	optionSet = {		'norm'				: bool(int(norm)),
						'log10'				: bool(int(log10))
				}
    
	updateOptions(optionSet)

	if plot == 'lms':
		return HttpResponse(mark_safe(webapi.table.lms(results, options, '')))

	elif plot == 'lms_base':
		return HttpResponse(mark_safe(webapi.table.lms_base(results, options, '')))

	elif plot == 'bm':
		return HttpResponse(mark_safe(webapi.table.bm(results, options, '')))

	elif plot == 'lm':
		return HttpResponse(mark_safe(webapi.table.lm(results, options, '')))

	elif plot == 'xyz':
		return HttpResponse(mark_safe(webapi.table.xyz(results, options, '')))

	elif plot == 'xy':
		return HttpResponse(mark_safe(webapi.table.xy(results, options, '')))
	
	elif plot == 'xyz_purples':
		return HttpResponse(mark_safe(webapi.table.xyz_purples(results, options, '')))

	elif plot == 'xy_purples':
		return HttpResponse(mark_safe(webapi.table.xyz_purples(results, options, '')))

	elif plot == 'xy31':
		return HttpResponse(mark_safe(webapi.table.xy31(results, options, '')))

	elif plot == 'xyz31':
		return HttpResponse(mark_safe(webapi.table.xyz31(results, options, '')))

	elif plot == 'xyz64':
		return HttpResponse(mark_safe(webapi.table.xyz64(results, options, '')))

	elif plot == 'xy64':
		return HttpResponse(mark_safe(webapi.table.xy64(results, options, '')))
		
	else:
		return HttpResponse('No table for plot %s' % plot)


def get_description(request, plot, norm, log10):
	results = request.session['results']
	
	optionSet = {		'norm'				: bool(int(norm)),
						'log10'				: bool(int(log10))
				}
    
	updateOptions(optionSet)

	if plot == 'lms':
		return HttpResponse(mark_safe(webapi.description.lms(results, '', options, '')))

	elif plot == 'lms_base':
		return HttpResponse(mark_safe(webapi.description.lms_base(results, '', options, '')))

	elif plot == 'bm':
		return HttpResponse(mark_safe(webapi.description.bm(results, '', options, '')))

	elif plot == 'lm':
		return HttpResponse(mark_safe(webapi.description.lm(results, '', options, '')))

	elif plot == 'xyz':
		return HttpResponse(mark_safe(webapi.description.xyz(results, '', options, '')))

	elif plot == 'xy':
		return HttpResponse(mark_safe(webapi.description.xy(results, '', options, '')))

	elif plot == 'xyz_purples':
		return HttpResponse(mark_safe(webapi.description.xyz_purples(results, '', options, '')))
	
	elif plot == 'xy_purples':
		return HttpResponse(mark_safe(webapi.description.xy_purples(results, '', options, '')))
	
	elif plot == 'xyz31':
		return HttpResponse(mark_safe(webapi.description.xyz31(results, '', options, '')))

	elif plot == 'xyz64':
		return HttpResponse(mark_safe(webapi.description.xyz64(results, '', options, '')))
		
	elif plot == 'xy31':
		return HttpResponse(mark_safe(webapi.description.xy31(results, '', options, '')))

	elif plot == 'xy64':
		return HttpResponse(mark_safe(webapi.description.xy64(results, '', options, '')))
		
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
			   	'cc'			: '%.1f, %.5f, %.5f, %.5f',

				'xyz_purples'   : '%.1f, %.5f, %.5f, %.5f',
				'xy_purples'   : '%.1f, %.5f, %.5f, %.5f'
	}

	plot_name = {
					'lms' 			: 'lms',
					'lms_base'		: 'lms_9figs',

					'bm'			: 'ls_mb',
					'lm'			: 'lm',

					'xyz' 			: 'xyz',
					'xy'			: 'xy',

					'xyz_purples'	: 'xyz_purples',
					'xy_purples'    : 'xy_purples',

					'xyz31' 		: 'xyz31',
					'xyz64' 		: 'xyz64',

					'xy31'			: 'xy31',
					'xy64'			: 'xy64',


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
    start      = time.time()
    field_size = float(field_size)
    age        = float(age)
    lambda_min = float(lambda_min)
    lambda_max = float(lambda_max)
    lambda_step= float(lambda_step)

    print('compute')

    request.session['results'], request.session['plots'] = webapi.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
    print('done')
    stop = time.time()
    log.debug("[%s] Compute performed in %s seconds - sID: %s" % ( time_now(), str(stop - start), request.session.session_key))

    return HttpResponse('Calculate fields updated')


def home(request):

	log.info("[%s] New request. sessionId: %s" % (time_now(), request.session.session_key))
	log.info("[%s] User Agent: %s" % (time_now(), request.META['HTTP_USER_AGENT']))

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
	request.session['results'], request.session['plots'] = webapi.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
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
