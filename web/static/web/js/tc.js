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


function axis_labels(x, y){
	this.x = x;
	this.y = y;
}
	
var axis_labels = ({ 	'xyz' 		: new axis_labels("Wavelength [nm]", "Fundamental tristimulus values"),
						'xy'		: new axis_labels("x<sub>F, " + currentForm['field_size'] + ", " + currentForm['age'] + "</sub>", 
													  "y<sub>F, " + currentForm['field_size'] + ", " + currentForm['age'] + "</sub>"),
													  
						'lms'		: new axis_labels("Wavelength [nm]", "Relative energy sensitivities"),
						'lms_base'	: new axis_labels("x_base", "y_base"),
						
						'bm'		: new axis_labels("l<sub>MB, " + currentForm['field_size'] + ", " + currentForm['age'] + "</sub>", 
													  "m<sub>MB, " + currentForm['field_size'] + ", " + currentForm['age'] + "</sub>"),
													  
						'lm'		: new axis_labels("l<sub>" + currentForm['field_size'] + ", " + currentForm['age'] + "</sub>",
													  "m<sub>" + currentForm['field_size'] + ", " + currentForm['age']+ "</sub>"),
						
						'xyz31'		: new axis_labels("Wavelength [nm]", "Fundamental tristimulus values"),
						
						'xy31'		: new axis_labels("x", "y"),
						
						'xyz64'		: new axis_labels("x", "y"),
});


var currentPlot = availablePlots[0]; //Current plot LMS
var plot_options = {
					 'grid' 		: 0,
					 'cie31'		: 0,
					 'cie64'		: 0,
					 'labels'		: 0
		}

//Plot title in HTML description.

for ( i=0; i < availablePlots.length; i++ ){
	$( "div#" + availablePlots[i] + "_html .description-heading-2" )
		.html($( "option[plot=" + availablePlots[i] + "]").html());

}

//Init labels

$( "div.x_label" ).html(axis_labels[availablePlots[0]].x);
$( "div.y_label" ).html(axis_labels[availablePlots[0]].y);

function getOptionsString(){
	return "" + plot_options.grid + plot_options.cie31 + plot_options.cie64 + plot_options.labels;
}

//This function retrieves a plot from the server via AJAX
function refreshPlot(plot){

 	var data = all_plots[plot].getPlot(getOptionsString());

	if (data == null) { //If data is not cached, get it from the server.
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
								$( "img#loader" ).hide(); //Hide spinning wheel
								$( "div.label" ).fadeIn(); //Show the labels
  							})
  							.fail(function() {
    							console.log( "error when getting " + plot + " plot from server" );
				});
	} else { //Present cached data.

		$( "div#" + plot + "_plot" ).empty();
		$( "div#" + plot + "_plot" ).append(data);
		$( "img#loader" ).hide(); //Hide spinning wheel
	}
}

//This will load all the plots.
function refreshAllPlots(){
	for (i=0; i < availablePlots.length; i++){
		refreshPlot(availablePlots[i]);
	}
}

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

//@TODO: Need to make navigation buttons (home, magnifier, cross) more visible.
	$( "image" ).css("opacity", 1); //To make the nav elements more visible.
	

//Start by showing first plot + data:

	$( "#" + availablePlots[0] + "_plot" ).show();
	$( "#" + availablePlots[0] + "_html" ).show();
	$( "#" + availablePlots[0] + "_table" ).show();


//Changing plots:

	$( "select#plot-select" ).on("keydown change", function(){

		var plot = $('option:selected', this).attr('plot');
		currentPlot = plot; //update current plot
		
		$( "div.plot" ).hide(); 				//Hide all plots
		$( "div.html_text" ).hide();			//Hide all HTML
		$( "div.table" ).hide();				//Hide all tables
		$( "div#" + plot + "_plot" ).show();	//Show selected plot
		$( "div#" + plot + "_html" ).show();	//Show selected HTML
		$( "div#" + plot + "_table" ).show();	//Show selected table
		
		$( "div.x_label" ).html(axis_labels[plot].x);
		$( "div.y_label" ).html(axis_labels[plot].y);
								
		updateCheckboxes(plot);
	});
	
	//Enable or disable checkboxes
	function updateCheckboxes(plot){	
		switch(plot){
			
			case "xyz":
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");;
				
			break;
			
			case "xy": // CIE xy fundamental chromacity diagram
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "lms": //CIE LMS cone fundamentals
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "lms_base": //CIE LMS cone fundamentals (9 sign.flgs.)
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "bm": //CIE MacLeod-Boynton ls diagram
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "lm": //Equi-power normalised lm diagram
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", true).prev().addClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
			case "xyz31": //Equi-power normalised lm diagram
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", true).prev().addClass("disabled");
				
			break;
			
			case "xy31": //Equi-power normalised lm diagram
				
				$( "#showGrid" ).prop("disabled", false).prev().removeClass("disabled");					
				$( "#compare1931-2" ).prop("disabled", true).prev().addClass("disabled");
				$( "#compare1964-10" ).prop("disabled", false).prev().removeClass("disabled");
				$( "#showLabels" ).prop("disabled", false).prev().removeClass("disabled");
				
			break;
			
		}
	}
	
	// Checkbox events (Bit ugly, but OK)
	
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
		refreshAllPlots();
	});
		

