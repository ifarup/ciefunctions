/* Script to manage tc web app */
$( window ).load(function(){

//Spinner init.

$( "input#age" ).spinner({	
							min: 20,
							max: 70,
							step: 1,
});

$( "input#field_size" ).spinner({
									min: 1.0,
									max: 10.0,
									step: .1
});

$( "input#lambda_min" ).spinner({
									min: 390.0,
									max: 400.0,
									step: .1
});

$( "input#lambda_max" ).spinner({
									min: 700.0,
									max: 830.0,
									step: .1
});

$( "input#lambda_step" ).spinner({
									min: 0.1,
									max: 5.0,
									step: .1,
									numberFormat: 'd'
});

//Show the global loader when ajax.
$( document ).ajaxStop(function() {
	$("div.velo").hide();
});

$( "button#btnCompute" ).on('click', function(){

	function flash(component){
		component
		.animate({backgroundColor: "rgb(255,0,0)"}, 500 )
		.animate({backgroundColor: "rgb(255,255,255)"}, 500 );
		return;
	}
	
	//Age
	min_age = parseInt($( "input#age" ).attr("aria-valuemin"));
	max_age = parseInt($( "input#age" ).attr("aria-valuemax"));
	age 	= parseInt($( "input#age" ).val());

	if (age < min_age){
		flash($( "input#age" ));
		$( "input#age" ).val(min_age);
		return false;
	} else if ( age > max_age ){
		flash($("input#age"));
		$( "input#age" ).val(max_age);
		return false;
	} else if ( isNaN(age) ){
		flash($("input#age"));
		$( "input#age" ).val(min_age);
		return false;
	}
	
	//field_size
	min_field_size 	= parseFloat($( "input#field_size" ).attr("aria-valuemin"));
	max_field_size 	= parseFloat($( "input#field_size" ).attr("aria-valuemax"));
	field_size 		= parseFloat($( "input#field_size" ).val()).toFixed(1);

	
	if (field_size < min_field_size){
		flash($( "input#field_size" ));
		$( "input#field_size" ).val(min_field_size);
		return false;
	} else if ( field_size > max_field_size ){
		flash($("input#field_size"));
		$( "input#field_size" ).val(max_field_size);
		return false;
	} else if ( isNaN(field_size) ){
		flash($("input#field_size"));
		$( "input#field_size" ).val(min_field_size);
		return false;
	}
	
	//lambda_min
	min_lambda_min 	= parseFloat($( "input#lambda_min" ).attr("aria-valuemin"));
	max_lambda_min 	= parseFloat($( "input#lambda_min" ).attr("aria-valuemax"));
	lambda_min 		= parseFloat($( "input#lambda_min" ).val());
	
	if ( lambda_min < min_lambda_min ){
		flash($( "input#lambda_min" ));
		$( "input#lambda_min" ).val(min_lambda_min);
		return false;
	} else if ( lambda_min > max_lambda_min ){
		flash($("input#lambda_min"));
		$( "input#lambda_min" ).val(max_lambda_min);
		return false;
	} else if ( isNaN(lambda_min) ){
		flash($("input#lambda_min"));
		$( "input#lambda_min" ).val(min_lambda_min);
		return false;
	}
	
	//lambda_max
	min_lambda_max 	= parseFloat($( "input#lambda_max" ).attr("aria-valuemin"));
	max_lambda_max 	= parseFloat($( "input#lambda_max" ).attr("aria-valuemax"));
	lambda_max 		= parseFloat($( "input#lambda_max" ).val());
	
	if ( lambda_max < min_lambda_max ){
		flash($( "input#lambda_max" ));
		$( "input#lambda_max" ).val(min_lambda_max);
		return false;
	} else if ( lambda_max > max_lambda_max ){
		flash($("input#lambda_max"));
		$( "input#lambda_max" ).val(max_lambda_max);
		return false;
	} else if ( isNaN(lambda_max) ){
		flash($("input#lambda_max"));
		$( "input#lambda_max" ).val(min_lambda_max);
		return false;
	}
	
	//lambda_step
	min_lambda_step 	= parseFloat($( "input#lambda_step" ).attr("aria-valuemin"));
	max_lambda_step 	= parseFloat($( "input#lambda_step" ).attr("aria-valuemax"));
	lambda_step 		= parseFloat($( "input#lambda_step" ).val());
	
	if ( lambda_step < min_lambda_step ){
		flash($( "input#lambda_step" ));
		$( "input#lambda_step" ).val(min_lambda_step);
		return false;
	} else if ( lambda_step > max_lambda_step ){
		flash($("input#lambda_step"));
		$( "input#lambda_step" ).val(max_lambda_step);
		return false;
	}  else if ( isNaN(lambda_step) ){
		flash($("input#lambda_step"));
		$( "input#lambda_step" ).val(min_lambda_step);
		return false;
	}

	//Trigger a new calculation
	ajaxUrl = 	"/compute/" 	+ 
				field_size 		+ "/" + 
				age 			+ "/" + 
				lambda_min		+ "/" +
				lambda_max		+ "/" +
				lambda_step		+ "/";

	$( "div.velo" ).show(); //We disable the page and show a loader.
	flushCache();
	$.get( ajaxUrl )
				.done(function( data ) {
					dontCache = true;
					refreshAllObjects();
					updateLabels();
					$( "div.x_label" ).html(axis_labels[currentPlot].x);
					$( "div.y_label" ).html(axis_labels[currentPlot].y);

  				}).fail(function() {
    				console.log( "error when calling compute." );
	});

	return false;

});

//Object definition for axis
function axis_label(x, y){
	this.x = x;
	this.y = y;
}

var axis_labels;

function updateLabels(){

var age = parseInt($( "input#age" ).val());
var field_size = parseInt($( "input#field_size" ).val());
var lambda_min = parseInt($( "input#lambda_min" ).val());
var lambda_max= parseInt($( "input#lambda_max" ).val());
var lambda_step = parseInt($( "input#lambda_step" ).val());

	axis_labels = ({ 	'xyz' 		: new axis_label("Wavelength [nm]", "Fundamental tristimulus values"),
						'xy'		: new axis_label("<span class='math'>x</span><sub>F, " + field_size + ", " + age + "</sub>", 
													  "y<sub>F, " + field_size + ", " + age + "</sub>"),
													  
						'lms'		: new axis_label("Wavelength [nm]", "Relative energy sensitivities"),
						'lms_base'	: new axis_label("Wavelength [nm]", "Relative energy sensitivities"),
						
						'bm'		: new axis_label("<span class='math'>l</span><sub>MB, " + field_size + ", " + age + "</sub>", 
													  "<span class='math'>m</span><sub>MB, " + field_size + ", " + age + "</sub>"),
													  
						'lm'		: new axis_label("<span class='math'>l</span><sub>" + field_size + ", " + age + "</sub>",
													  "<span class='math'>m</span><sub>" + field_size + ", " + age + "</sub>"),
						
						'xy31'		: new axis_label("<span class='math'>x</span>", "<span class='math'>y</span>"),
						'xy64'		: new axis_label("<span class='math'>x</span>", "<span class='math'>y</span>"),
						
						'xyz31'		: new axis_label("Wavelength [nm]", "Fundamental tristimulus values"),
						'xyz64'		: new axis_label("Wavelength [nm]", "Fundamental tristimulus values"),
						
	});

}

//Object for plotting options
var plot_options = {
					 'grid' 		: 0,
					 'cie31'		: 0,
					 'cie64'		: 0,
					 'labels'		: 0
		}

//Init
var currentPlot = availablePlots[0]; //Current plot LMS
$( "#descriptionTitle" ).html($( "option[plot=" + currentPlot + "]").html());
updateLabels();
$( "div.x_label" ).html(axis_labels[currentPlot].x);
$( "div.y_label" ).html(axis_labels[currentPlot].y);
$( "div#std-params" ).hide();


function getOptionsString(){
	return "" + plot_options.grid + plot_options.cie31 + plot_options.cie64 + plot_options.labels;
}

//This function retrieves an object (table or description, file an issue for plot)
function refreshObject(object, name){
/* object is a String: can be 'table' or 'description'*/
	$( "div.velo" ).show();
	ajaxUrl = '/get_'+ object + '/' + name + '/';

	$.get( ajaxUrl )
				.done(function( data ) {
					$( "div#" + name + "_" + object ).empty();
					$( "div#" + name + "_" + object ).append(data);
  				}).fail(function() {
    				console.log( "error when getting " + name + " " + object + " from server" );
	});
}

//This will load all the tables and descriptions.
function refreshAllObjects(){
	for (i=0; i < availablePlots.length; i++){
		refreshObject('table', availablePlots[i]);
		refreshObject('description', availablePlots[i]);
		refreshPlot(availablePlots[i]);
	}
}

//This function retrieves a plot from the server via AJAX

function refreshPlot(plot){
 	var data = all_plots[plot].getPlot(getOptionsString());
	$( "div.velo" ).show();
	if ((data == null)) { //If data is not cached, get it from the server.
					$.get( '/get_plot/' + 
						plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.cie31 + "/" + 
						plot_options.cie64 + "/" + 
						plot_options.labels + "/" )
							.done(function( data ) {
								all_plots[plot].setPlot(getOptionsString(), data); //Cache plot
								$( "div#" + plot + "_plot" ).empty();
								$( "div#" + plot + "_plot" ).append(data);
								$( ".mpld3-toolbar image" ).css("opacity", 1); //Remove transparency for toolbar buttons.
  							})
  							.fail(function() {
    							console.log( "error when getting " + plot + " plot from server" );
				});
	} else { //Present cached data.
		$( "div#" + plot + "_plot" ).empty();
		$( "div#" + plot + "_plot" ).append(data);
		$( "div.velo" ).hide();
	}
}

//This function sends table data to the user

$( "button#getCsv" ).on("click", function(){
	location.href = "/get_csv/" + currentPlot + "/";
});


//This will load all the plots EXCEPT for 'plot'.
function refreshAllOthers(plot){
	for (i=0; i < availablePlots.length; i++){
		if ( availablePlots[i] != plot ){
			refreshPlot(availablePlots[i]);
		}
	}
}

//Initialization of jQuery UI tabs

	$( "#tc-Tabs" ).tabs({
					heightStyle: "content",
					});
	
	$( "#tc-Tabs" ).css({'height': 'auto', 'width': 'auto'});
	
//And button
	$( "button#btnCompute" ).button();

//Save table

	$( "button#getCsv" ).button();

//@TODO: Need to make navigation buttons (home, magnifier, cross) more visible.
	$( "image" ).css("opacity", 1); //To make the nav elements more visible.
	

//Start by showing first plot + data:

	$( "#" + availablePlots[0] + "_plot" ).show();
	$( "#" + availablePlots[0] + "_description" ).show();
	$( "#" + availablePlots[0] + "_table" ).show();


//Changing plots:

	$( "select#plot-select" ).on("keydown change", function(){

		var plot = $('option:selected', this).attr('plot');
		currentPlot = plot; //update current plot
		
		$( "div.plot" ).hide(); 				//Hide all plots
		$( "div.html_text" ).hide();			//Hide all HTML
		$( "div.table" ).hide();				//Hide all tables
		$( "div#" + plot + "_plot" ).show();	//Show selected plot
		$( "div#" + plot + "_description" ).show();	//Show selected HTML
		$( "div#" + plot + "_table" ).show();	//Show selected table
		$( "#descriptionTitle" ).html($( "option[plot=" + plot + "]").html());
		$( "div.x_label" ).html(axis_labels[plot].x);
		$( "div.y_label" ).html(axis_labels[plot].y);

		updateCheckboxes(plot);
		refreshAllObjects();
	});
	
	
//Showing standard plots

function showStandard( standard_plot ){
	var data = all_plots[standard_plot].getPlot(getOptionsString());
	console.log("loading " + standard_plot);
	currentPlot = standard_plot;
	
	$( "div.plot" ).hide(); 				//Hide all plots
	$( "div.html_text" ).hide();			//Hide all HTML
	$( "div.table" ).hide();				//Hide all tables
	$( "div#" + standard_plot + "_plot" ).show();	//Show selected plot
	$( "div#" + standard_plot + "_description" ).show();	//Show selected HTML
	$( "div#" + standard_plot + "_table" ).show();	//Show selected table
	$( "#descriptionTitle" ).html($( "option[plot=" + standard_plot + "]").html());
	$( "div.x_label" ).html(axis_labels[standard_plot].x);
	$( "div.y_label" ).html(axis_labels[standard_plot].y);
	
	$( "div.velo" ).show();
	if ((data == null)) { //If data is not cached, get it from the server.
					$.get( '/get_plot/' + 
						standard_plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.cie31 + "/" + 
						plot_options.cie64 + "/" + 
						plot_options.labels + "/" )
							.done(function( data ) {
								all_plots[standard_plot].setPlot(getOptionsString(), data); //Cache plot
								$( "div#" + standard_plot + "_plot" ).empty();
								$( "div#" + standard_plot + "_plot" ).append(data);
								$( ".mpld3-toolbar image" ).css("opacity", 1); //Remove transparency for toolbar buttons.
  							})
  							.fail(function() {
    							console.log( "error when getting " + standard_plot + " plot from server" );
				});
	} else { //Present cached data.
		$( "div#" + standard_plot + "_plot" ).empty();
		$( "div#" + standard_plot + "_plot" ).append(data);
		$( "div.velo" ).hide();
	}
}	
	
//Changing standard plots:

	$( "select#field_size" ).on('keydown change', function(){

		var year = $( 'option:selected', this ).attr('year');
		var plot = $( 'option:selected', ( "select#plot-select" ) ).attr('plot');
		
		plot = plot.replace("64", "");
		plot = plot.replace("31", "");
		standard_plot = plot + year;
		
		switch (year){
			case "31":
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				showStandard(standard_plot);
				
			break;
		
			case "64":
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				showStandard(standard_plot);
			break;
		}

		refreshPlot(standard_plot);
	});
	
	//Enable or disable checkboxes
	function updateCheckboxes(plot){
		switch(plot){
			
			case "xyz":
				$( "div#std-params" ).hide();				
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");;
				
			break;
			
			case "xy": // CIE xy fundamental chromacity diagram
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
								
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "lms": //CIE LMS cone fundamentals
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
								
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "lms_base": //CIE LMS cone fundamentals (9 sign.flgs.)
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "bm": //CIE MacLeod-Boynton ls diagram
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
				
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "lm": //Equi-power normalised lm diagram
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "528px");
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "xyz31": //Equi-power normalised lm diagram
				$( "div#std-params" ).show();
				$( "div#input-params").hide();
				$( "div.htmlWrapper").css("height", "600px");
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "xy31": //CIE xy standard chromaticity diagram
				$( "div#std-params" ).show();
				$( "div#input-params").hide();
				$( "div.htmlWrapper").css("height", "600px");
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
		}
	}
	
	// Checkbox events (Bit ugly, but OK)
				$( "input[type=checkbox]" ).on('click', function(){
					$( "div.velo" ).show();
					console.log($(this));
				});
	
				$( "#showGrid" ).on("click", function(){
					if (plot_options.grid==1) {
						plot_options.grid = 0;
					} else {
						plot_options.grid = 1;
					}
					
					refreshPlot(currentPlot);
					refreshAllOthers(currentPlot);
					
				});					
				$( "#compare1931-2" ).on("click", function(){
					if (plot_options.cie31==1) {
						plot_options.cie31 = 0;
					} else {
						plot_options.cie31 = 1;
					}
					refreshPlot(currentPlot);
					refreshAllOthers(currentPlot);
					
				});
				$( "#compare1964-10" ).on("click", function(){
					if (plot_options.cie64==1) {
						plot_options.cie64 = 0;
					} else {
						plot_options.cie64 = 1;
					}
					refreshPlot(currentPlot);
					refreshAllOthers(currentPlot);
					
				});
				$( "#showLabels" ).on("click", function(){
					if (plot_options.labels==1) {
						plot_options.labels = 0;
					} else {
						plot_options.labels = 1;
					}
					refreshPlot(currentPlot);
					refreshAllOthers(currentPlot);
					
				});
		refreshAllObjects();
	});
		

