/* Script to manage tc web app */
$( ).ready(function(){	

//Load the default plots via ajax:
	

var availablePlots = [ 'xyz', 'xy', 'lms', 'lms_base', 'bm', 'lm' ];

function axis_labels(x, y){
	this.x = x;
	this.y = y;
}

var currentPlot = availablePlots[0];
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

//This function retrieves a plot from the server via AJAX
function refreshPlot(plot){
		console.log("refreshPlot: " + plot);
				$.get( '/get_plot/' + 
						plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.cie31 + "/" + 
						plot_options.cie64 + "/" + 
						plot_options.labels + "/" )
							.done(function( data ) {
								$( "div#" + plot + "_plot" ).empty();
								$( "div#" + plot + "_plot" ).append(data);
								$( "img#loader" ).hide(); //Hide spinning wheel
  							})
  							.fail(function() {
    							console.log( "error when getting " + plot + " plot from server" );
				});
}

//This will load all the plots from the server.
function refreshAllPlots(){
	for (i=0; i < availablePlots.length; i++){
		refreshPlot(availablePlots[i]);
	}
}

//This will load all the plots EXCEPT for 'plot'
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
	

//Start by showing XYZ plot + data:

	$( "#xyz_plot" ).show();
	$( "#xyz_html" ).show();
	$( "#xyz_table" ).show();


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
	
		updateCheckboxes(plot);
	});
	
	//Enable or disable checkboxes
	function updateCheckboxes(plot){	
		switch(plot){
			
			case "xyz":
				
				$( "#showGrid" ).prop("disabled", false);
				$( "#compare1931-2" ).prop("disabled", false);
				$( "#compare1964-10" ).prop("disabled", false);
				$( "#showLabels" ).prop("disabled", true);
				
			break;
			
			case "xy": // CIE xy fundamental chromacity diagram
				
				$( "#showGrid" ).prop("disabled", false);
				$( "#compare1931-2" ).prop("disabled", false);
				$( "#compare1964-10" ).prop("disabled", false);
				$( "#showLabels" ).prop("disabled", false);
				
			break;
			
			case "lms": //CIE LMS cone fundamentals
				
				$( "#showGrid" ).prop("disabled", false);
				$( "#compare1931-2" ).prop("disabled", true);
				$( "#compare1964-10" ).prop("disabled", true);
				$( "#showLabels" ).prop("disabled", true);
				
			break;
			
			case "lms_base": //CIE LMS cone fundamentals (9 sign.flgs.)
				
				$( "#showGrid" ).prop("disabled", false);
				$( "#compare1931-2" ).prop("disabled", true);
				$( "#compare1964-10" ).prop("disabled", true);
				$( "#showLabels" ).prop("disabled", true);
				
			break;
			
			case "bm": //CIE MacLeod-Boynton ls diagram
				
				$( "#showGrid" ).prop("disabled", false);
				$( "#compare1931-2" ).prop("disabled", true);
				$( "#compare1964-10" ).prop("disabled", true);
				$( "#showLabels" ).prop("disabled", false);
				
			break;
			
			case "lm": //Equi-power normalised lm diagram
				
				$( "#showGrid" ).prop("disabled", false);					
				$( "#compare1931-2" ).prop("disabled", true);
				$( "#compare1964-10" ).prop("disabled", true);
				$( "#showLabels" ).prop("disabled", false);
				
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
		

