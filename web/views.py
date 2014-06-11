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
#from numpy import *
import numpy as np
import StringIO

from web.models import Result, Plot
from django.shortcuts import get_object_or_404

from django.utils import simplejson as json

import logging
log = logging.getLogger(__name__)

def get_plot(request, plot, grid, cie31, cie64, labels):
	log.debug("Requesting %s/%s/%s/%s/%s" % (plot, grid, cie31, cie64, labels))
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
	
	elif (plot == 'xyz31'):
		tc182.plot.xyz31(ax, plots, options)
	
	elif (plot == 'xy31'):
		tc182.plot.xy31(ax, plots, options)
	
	theFig = mark_safe(mpld3.fig_to_html(fig, template_type='general'))
	resulting_plot = theFig;
	plt.close(fig)
	return HttpResponse(resulting_plot);

def get_csv(request, plot):

	
	format = { 'xyz' 		:  '%.1f, %.6e, %.6e, %.6e',
			   'lms' 		: '%.1f, %.5e, %.5e, %.5e',
			   'lms_base'	: '%.1f, %.8e, %.8e, %.8e',
			   'bm'			: '%.1f, %.6f, %.6f, %.6f',
			   'lm'			: '%.1f, %.6f, %.6f, %.6f',
			   'cc'			: '%.1f, %.5f, %.5f, %.5f'
	}

	plot = str(plot)
	output = StringIO.StringIO()
	thePlot = request.session['results']
	np.savetxt(output, thePlot[plot], format[plot])
	response = HttpResponse(output.getvalue(), mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename = "%s.csv"' % plot
	return response

def home(request):

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
		
		
	log.debug("Age: %s, field_size: %s, lambda_min: %s, lambda_max: %s, lambda_step: %s"
				% ( age, field_size, lambda_min, lambda_max, lambda_step))
				
	html_list = [] #List containing all the theDescriptions
	tab_list = []  #List containing all the tabulated data
	
	try:
		serialized_test_results = Result.objects.get(field_size=field_size, age=age, lambda_min=lambda_min, lambda_max=lambda_max, lambda_step=lambda_step)
		test_results = json.loads(serialized_test_results)
		request.session['results'] = test_results.get_data()
		results = test_results.get_data()
	
		serialized_test_plots = Plot.objects.get(field_size=field_size, age=age, lambda_min=lambda_min, lambda_max=lambda_max, lambda_step=lambda_step)
		test_plot = serializers.loads(serialized_test_plots)
		request.session['plots'] = test_plots.get_data()
		plots = test_plots.get_data()
		
	except Exception as e:
		print "1st try %s" % e
		print "Computing ..."
		results, plots = tc182.compute_tabulated(field_size, age, lambda_min, lambda_max, lambda_step)
		request.session['results'] = results
		request.session['plots'] = plots
		
		try:
			serialized_results = json.dumps(results)
			#new_result = Result( 	field_size=field_size, 
			#						age=age, 
			#						lambda_min=lambda_min, 
			#						lambda_max=lambda_max, 
			#						lambda_step=lambda_step, 
			#						data=serialized_results )
			#new_result.save()
		except Exception as e:
			print "Can't serialize results: %s" % e
			
		try:
			serialized_plots = json.dumps(plots)
			#new_plot = Plot ( 	field_size=field_size,
			#					age=age, 
			#					lambda_min=lambda_min, 
			#					lambda_max=lambda_max, 
			#					lambda_step=lambda_step, 
			#					data=plots )
			#new_plot.save()
		except Exception as e:
			print "Can't serialize plots: %s" % e
			print e
		
    #0 #xyz 
	
	theDescription = mark_safe(tc182.description.xyz(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xyz(results));
	tab_list.append(theTable)
	
    #1 #xy
	
	theDescription = mark_safe(tc182.description.xy(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xy(results));
	tab_list.append(theTable)

	
	#2 #lms
	
	theDescription = mark_safe(tc182.description.lms(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lms(results));
	tab_list.append(theTable)

	
	#3 #lms_base
    
	theDescription = mark_safe(tc182.description.lms_base(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lms_base(results));
	tab_list.append(theTable)

	#4 #bm
	
	theDescription = mark_safe(tc182.description.bm(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.bm(results));
	tab_list.append(theTable)

	#5 #lm
	
	theDescription = mark_safe(tc182.description.lm(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.lm(results));
	tab_list.append(theTable)
	
	#6 xyz31 (CHECK THIS ONE!!!)
	
	theDescription = mark_safe(tc182.description.xyz31(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xyz31(results));
	tab_list.append(theTable)
	
	#xy31 (AND THIS ONE!!)
	
	theDescription = mark_safe(tc182.description.xy31(results, ''))
	html_list.append(theDescription)
	
	theTable = mark_safe(tc182.table.xy31(results));
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