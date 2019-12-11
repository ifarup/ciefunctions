/* Script to manage tc web app */
	//Spinner init.
	
$(function(){

	$( "input#age" ).spinner({	
			min: 20,
			max: 70,
			step: 1
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

});

$( ".ui-spinner" ).width("70px");

$( ".ui-spinner-input" ).width("40px");


//Hide the global loader when ajaxStop.
$( document ).ajaxStop(function() {
	$("div.velo").hide();
    if (typeof MathJax != "undefined") {
	   MathJax.Hub.Typeset();
    }
    $( ".x_label, .y_label" ).show();
    adjustLabelPos();
    updateCheckboxes(currentPlot);
});


$( "button#btnCompute" ).on('click', function(){
	
	$( ".velo" ).show(); //All velo's up!
	
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

	flushCache();
	$.get( ajaxUrl )
				.done(function() {
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
var field_size = parseFloat($( "input#field_size" ).val());
var lambda_min = parseInt($( "input#lambda_min" ).val());
var lambda_max= parseInt($( "input#lambda_max" ).val());
var lambda_step = parseInt($( "input#lambda_step" ).val());

	axis_labels = ({
        				'lms'		: new axis_label("Wavelength (nm)",
							                         "Relative energy sensitivities"),

        				'lms_base'	: new axis_label("Wavelength (nm)", "Relative energy sensitivities"),

        				'bm'		: new axis_label("<span class='math'>l</span><sub>MB, " + field_size + ", " + age + "</sub>",
							                         "<span class='math'>s</span><sub>MB, " + field_size + ", " + age + "</sub>"),

        				'lm'		: new axis_label("<span class='math'>l</span><sub>" + field_size + ", " + age + "</sub>",
												     "<span class='math'>m</span><sub>" + field_size + ", " + age + "</sub>"),

						'xyz' 		: new axis_label("Wavelength [nm]", "Cone-fundamental-based tristimulus values"),
						'xy'		: new axis_label("<span class='math'>x</span><sub>F, " + field_size + ", " + age + "</sub>", 
													  "y<sub>F, " + field_size + ", " + age + "</sub>"),

						'xy31'		: new axis_label("<span class='math'>x</span>", "<span class='math'>y</span>"),
						'xy64'		: new axis_label("<span class='math'>x<sub>10</sub></span>", "<span class='math'>y<sub>10</sub></span>"),
						
						'xyz31'		: new axis_label("Wavelength [nm]", "Tristimulus values"),
						'xyz64'		: new axis_label("Wavelength [nm]", "Tristimulus values"),

        				'xyz_purples'		: new axis_label("Complementary wavelength (nm)", "Cone-fundamental-based tristimulus Values"),
        				'xy_purples'		: new axis_label("<span class='math'>x</span><sub>F, " + field_size + ", " + age + "</sub>",
                            								 "y<sub>F, " + field_size + ", " + age + "</sub>")
	});

}

//Object for plotting options
var plot_options = {
					 'grid' 		: 0,
					 'cie31'		: 0,
					 'cie64'		: 0,
					 'labels'		: 0,
					 'norm'			: 0,
	                 'log10'        : 0,
};

//Init
var currentPlot = availablePlots[0]; //Current plot LMS
$( "#descriptionTitle" ).html($( "option[plot=" + currentPlot + "]").html());
this.updateLabels();
$( "div.x_label" ).html(axis_labels[currentPlot].x);
$( "div.y_label" ).html(axis_labels[currentPlot].y);
$( "div#std-params" ).hide();
$( ".renormalised-divz" ).hide();

function getOptionsString(){
	return "" + plot_options.grid + plot_options.cie31 + plot_options.cie64 + plot_options.labels + plot_options.norm + plot_options.log10;
}

function updatePlotOptions() {
	if ($("#showGrid")[0].checked) {
		plot_options.grid = 1;
	} else {
		plot_options.grid = 0;
	}

    if ($("#showLabels")[0].checked) {
		plot_options.labels = 1;
	} else {
		plot_options.labels = 0;
	}

	if ($("#renormalised")[0].checked) {
		plot_options.norm = 1;
	} else {
        plot_options.norm = 0;
	}

	if ($("#compare1931-2")[0].checked) {
		plot_options.cie31 = 1;
	} else {
        plot_options.cie31 = 0;
	}

    if ($("#compare1964-10")[0].checked) {
        plot_options.cie64 = 1;
    } else {
        plot_options.cie64 = 0;
    }
}

//This function retrieves an object (table or description, file an issue for plot)
function refreshObject(object, name){
	updatePlotOptions();
/* object is a String: can be 'table' or 'description'*/
	$( "div#" + name + "_" + object ).siblings(".velo").show();
	ajaxUrl = '/get_'+ object + '/' + name + '/' + plot_options.norm + "/" + plot_options.log10 + "/";
	$.get( ajaxUrl )
				.done(function( data ) {
					$( "div#" + name + "_" + object ).empty();
					$( "div#" + name + "_" + object ).append(data);
					$( "div#" + name + "_" + object ).siblings(".velo").hide();
					
					if ( $( 'table tr:last-of-type>td:first' ).text() != $( "input#lambda_max" ).val() ){

					//	if ($.isNumeric($( "input#lambda_max" ).val())){ 					
							$( "input#lambda_max" )
								.val( $( 'table tr:last-of-type>td:first' ).text() )
								.animate({backgroundColor: "rgba(225,127,80,.5)"}, 500 )
								.animate({backgroundColor: "rgba(255,255,255,.5)"}, 500 );	
					//	}

					}
					
					
					
  				}).fail(function() {
    				console.log( "error when getting " + name + " " + object + " from server" );
					$( "div#" + name + "_" + object ).siblings(".velo").hide();
	});
}

//This will load all the tables and descriptions.
function refreshAllObjects(){
    updatePlotOptions();
	for (i=0; i < availablePlots.length; i++){
		refreshObject('table', availablePlots[i]);
		refreshObject('description', availablePlots[i]);
		refreshPlot(availablePlots[i]);
		updateLabels();
        if (typeof MathJax != "undefined") {
		  MathJax.Hub.Typeset();
        }
	}
}

//This function retrieves a plot from the server via AJAX

function refreshPlot(plot){
    updatePlotOptions();
 	var data = all_plots[plot].getPlot(getOptionsString());
	$( "#theFig .velo" ).show();

	if ((data == null)) { //If data is not cached, get it from the server.
					$.get( '/get_plot/' + 
						plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.cie31 + "/" + 
						plot_options.cie64 + "/" + 
						plot_options.labels + "/" +
						plot_options.norm + "/" +
                        plot_options.log10 + "/")
							.done(function( data ) {
								all_plots[plot].setPlot(getOptionsString(), data); //Cache plot
								$( "div#" + plot + "_plot" ).empty();
								$( "div#" + plot + "_plot" ).append(data + '<div class="velo"></div>');
								//$( ".mpld3-toolbar image" ).css("opacity", 1); //Remove transparency for toolbar buttons.
								$( "div#" + plot + "_plot" ).siblings(".velo").hide();
  							})
  							.fail(function() {
    							console.log( "error when getting " + plot + " plot from server" );
				});
	} else { //Present cached data.
		$( "div#" + plot + "_plot" ).empty();
		$( "div#" + plot + "_plot" ).append(data);
		$( "#theFig .velo" ).hide();
        updateCheckboxes(currentPlot);
	}
}

//This function sends table data to the user

$( "button#getCsv" ).on("click", function(){
	location.href = "/get_csv/" + currentPlot + "/";
});


//This will load all the plots EXCEPT for 'plot'.
function refreshAllOthers(plot){
    updatePlotOptions();
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

	$( "image" ).css("opacity", 1); //To make the nav elements more visible.
	

//Start by showing first plot + data:

	$( "#" + availablePlots[0] + "_plot" ).show();
	$( "#" + availablePlots[0] + "_description" ).show();
	$( "#" + availablePlots[0] + "_table" ).show();

//Changing plots:

	$( "select#plot-select" ).on("keydown change", function(){
        updatePlotOptions();
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

		refreshAllObjects();
	});
	
	
//Showing standard plots

function showStandard( standard_plot ){
    updatePlotOptions();
	var data = all_plots[standard_plot].getPlot(getOptionsString());
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
	$( "#theFig .velo" ).show();
	if ((data == null)) { //If data is not cached, get it from the server.
					$.get( '/get_plot/' + 
						standard_plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.cie31 + "/" + 
						plot_options.cie64 + "/" + 
						plot_options.labels + "/" +
						plot_options.norm + "/" +
					    plot_options.log10 + "/")
							.done(function( data ) {
								all_plots[standard_plot].setPlot(getOptionsString(), data); //Cache plot
								$( "div#" + standard_plot + "_plot" ).empty();
								$( "div#" + standard_plot + "_plot" ).append(data);
								//$( ".mpld3-toolbar image" ).css("opacity", 1); //Remove transparency for toolbar buttons.
  							})
  							.fail(function() {
    							console.log( "error when getting " + standard_plot + " plot from server" );
					});
	} else { //Present cached data.
		$( "div#" + standard_plot + "_plot" ).empty();
		$( "div#" + standard_plot + "_plot" ).append(data);
		$( "#theFig .velo" ).hide();
	}
}	
	
//Changing standard plots:

	$( "select#field_size_year" ).on('keydown change', function(){
        updatePlotOptions();

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
				//$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				showStandard(standard_plot);
				
			break;
		
			case "64":
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				//$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				showStandard(standard_plot);
			break;
		}
		refreshObject("description", standard_plot);
		refreshObject("table", standard_plot);
		refreshPlot(standard_plot);
	});
	
	//Enable or disable checkboxes
	function updateCheckboxes(plot){

        //Enable all first and then disable/hide depending on the plot
		$( "#renormalised" ).show();
        $( "input[type=checkbox]" ).attr("disabled", false).removeClass("disabled"); //Enable all checkboxes
		switch(plot){

            case "lms":
                //console.log("CIE LMS cone fundamentals");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).hide();
                $( ".logarithmic-divz").show();

            break;

            case "lms_base":
                //console.log("CIE LMS cone fundamentals (9 sign.flgs.)");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).hide();
                $( ".logarithmic-divz" ).show();
            break;

			case "bm":
                //console.log("CIE MacLeod-Boynton ls diagram");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", true).prev().addClass("disabled"); //This is disabled because of a JSON parsing error at the backend.

                $( ".renormalised-divz" ).hide();
                $( ".logarithmic-divz" ).hide();
            break;

            case "lm":
                //console.log("Maxwellian lm chromaticity diagram");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", false).prev().removeClass("disabled");

                $( ".renormalised-divz" ).show();
                //but
                $( "#renormalised" ).hide();
                $( ".logarithmic-divz" ).hide();
                break;

			case "xyz":
                //console.log("CIE XYZ cone-fundamental-based tristimulus functions");
				$( "div#std-params" ).hide();				
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "80vh");
				
                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).show();
                $( ".logarithmic-divz" ).hide();
				
			break;
			
			case "xy":
                //console.log("CIE xy cone-fundamental-based chromaticity diagram");
				$( "div#std-params" ).hide();
				$( "div#input-params").show();
				$( "div.htmlWrapper").css("height", "80vh");
								
				$( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).attr("disabled", false).prev().removeClass("disabled");

                $( ".renormalised-divz" ).show();
                $( ".logarithmic-divz" ).hide();
			break;

			case "xyz_purples":
				//console.log("XYZ cone-fundamental-based tristimulus functions for purple-line stimuli");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).show();
                $( ".logarithmic-divz" ).hide();
            break;

            case "xy_purples":
                //console.log("xy cone-fundamental-based chromaticity diagram (purple-line stimuli)");
                $( "div#std-params" ).hide();
                $( "div#input-params").show();
                $( "div.htmlWrapper").css("height", "80vh");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", false).prev().removeClass("disabled");

                $( ".renormalised-divz" ).show();
                $( ".logarithmic-divz" ).hide();
            break;
			
			case "xyz31":
                //console.log("CIE XYZ standard colour-matching functions");
				$( "div#std-params" ).show();
				$( "div#input-params").hide();
				$( "div.htmlWrapper").css("height", "600px");
				$( "select#field_size_year option[year=31]" ).attr("selected", "true");
				
				$( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).hide();
                $( ".logarithmic-divz" ).hide();
			break;
			
			case "xy31":
                //console.log("CIE xy standard chromaticity diagram");
				$( "div#std-params" ).show();
				$( "div#input-params").hide();
				$( "div.htmlWrapper").css("height", "600px");
				$( "select#field_size_year option[year=31]" ).attr("selected", "true");
				
				$( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).attr("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).attr("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).attr("disabled", false).prev().removeClass("disabled");
				
				$( ".norm-div" ).hide();
                $( ".logarithmic-divz" ).hide();
			break;

            case "xyz64":
                //console.log("CIE XYZ standard colour-matching functions");
                $( "div#std-params" ).show();
                $( "div#input-params").hide();
                $( "div.htmlWrapper").css("height", "600px");
                $( "select#field_size_year option[year=31]" ).attr("selected", "true");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", true).prev().addClass("disabled");

                $( ".renormalised-divz" ).hide();
                $( ".logarithmic-divz" ).hide();
                break;

            case "xy64":
                //console.log("CIE xy standard chromaticity diagram")
                $( "div#std-params" ).show();
                $( "div#input-params").hide();
                $( "div.htmlWrapper").css("height", "600px");
                $( "select#field_size_year option[year=31]" ).attr("selected", "true");

                $( "#showGrid" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1931-2" ).attr("disabled", false).prev().removeClass("disabled");
                $( "#compare1964-10" ).attr("disabled", true).prev().addClass("disabled");
                $( "#showLabels" ).attr("disabled", false).prev().removeClass("disabled");

                $( ".norm-div" ).hide();
                $( ".logarithmic-divz" ).hide();
                break;
		}
	}
	
	// Checkbox events (Bit ugly, but OK)		

	$( "input[type=checkbox]" ).on('click', function(){
		//Disabling the checkboxes so the user doesn't click on them before the ajax call with the plot comes back. Clearing with updateCheckboxes().
		$( "input[type=checkbox]" ).attr("disabled", true); //Disable all checkboxes
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
			
	$( "#renormalised" ).on("click", function(){
		if (plot_options.norm==1) {
			plot_options.norm = 0;
		} else {
			plot_options.norm = 1;
		}

		if (currentPlot=="lm") {
			plot_options.norm = 1;
		}

		refreshPlot(currentPlot);
		refreshAllObjects();
	});

	$( "#logarithmic" ).on("click", function(){
		if (plot_options.log10==1) {
			plot_options.log10 = 0;
		} else {
			plot_options.log10 = 1;
		}
		refreshPlot(currentPlot);
		refreshAllObjects();
	});

$( function(){
		$( "button#btnCompute" ).trigger("click");
});

//Help function
$( function(){
    $( "div#helpButton a" ).click(function(){
        $( "#tabSys li" ).removeClass("active");
        $( "#tablePanel, #plotPanel").removeClass("active");
        $( "#helpPanel" ).addClass("active");
    });
});

//Move labels away from points
function adjustLabelPos(){
    var amountInPix = 15;
    $( "text.mpld3-text" ).each(function(){     
        $( this ).attr("x", parseInt($( this ).attr("x")) + amountInPix);
    });
}



