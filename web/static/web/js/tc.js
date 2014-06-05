/* Script to manage tc web app */
$( ).ready(function(){	





//Load the default plots via ajax:
	

var availablePlots = [ 'xyz', 'xy', 'lms', 'lms_base', 'bm', 'lm' ];
var plot_options = {
					 'grid' 		: 0,
					 'full_title'	: 0,
					 'cie31'		: 0,
					 'cie64'		: 0,
					 'labels'		: 0
		}

//Plot title in HTML description.

for ( i=0; i < availablePlots.length; i++ ){
	$( "div#" + availablePlots[i] + "_html .description-heading-2" )
		.html($( "option[plot=" + availablePlots[i] + "]").html());

}


//@TODO: Need to asynch this. I will repeat the code for now:


//xyz
			$.get( "/get_plot/" + availablePlots[0] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[0] +"_plot" ).append(data);
					$( "img#loader" ).hide(); //Hide spinning wheel
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[0] + " plot from server" );
				});	

//xy
			$.get( "/get_plot/" + availablePlots[1] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[1] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[1] + " plot from server" );
				});	

//lms
			$.get( "/get_plot/" + availablePlots[2] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[2] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[2] + " plot from server" );
				});	

// lms_base
			$.get( "/get_plot/" + availablePlots[3] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[3] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[3] + " plot from server" );
				});	

//bm
			$.get( "/get_plot/" + availablePlots[4] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[4] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[4] + " plot from server" );
				});	

//lm

			$.get( "/get_plot/" + availablePlots[5] + "/0/0/0/0/0/")
				.done(function( data ) {
					$( "div#" + availablePlots[5] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[5] + " plot from server" );
				});	

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

	$( "select#plot-select" ).on("change", function(){
		console.log("change");
		var plot = $('option:selected', this).attr('plot');
		
		$( "div.plot" ).hide(); 				//Hide all plots
		$( "div.html_text" ).hide();			//Hide all HTML
		$( "div.table" ).hide();				//Hide all tables
		$( "div#" + plot + "_plot" ).show();	//Show selected plot
		$( "div#" + plot + "_html" ).show();	//Show selected HTML
		$( "div#" + plot + "_table" ).show();	//Show selected table
		
		//Enable or disable checkboxes
		
		function enableAll(){
			$( "#figOptions input" ).prop("disabled", false);
		}
		
		function refreshPlot(plot){
				
				$.get( '/get_plot/' + 
						plot + '/' + 
						plot_options.grid + "/" + 
						plot_options.full_title + "/" +
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
		
		//Remove all previously assigned event listeners.
		
		$( "#figOptions input" ).off("click");
		
		
		switch(plot){
			
			case "xyz":
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", false)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", false)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				
				$( "#showLabels" ).prop("disabled", true)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})

				
			break;
			
			case "xy": // CIE xy fundamental chromacity diagram
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", false)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", false)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				
				$( "#showLabels" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})
			
			break;
			
			case "lms": //CIE LMS cone fundamentals
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", true)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", true)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				
				$( "#showLabels" ).prop("disabled", true)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})
			break;
			
			case "lms_base": //CIE LMS cone fundamentals (9 sign.flgs.)
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", true)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", true)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#showLabels" ).prop("disabled", true)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})

			break;
			
			case "bm": //CIE MacLeod-Boynton ls diagram
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", true)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", true)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				
				$( "#showLabels" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})
			break;
			
			case "lm": //Equi-power normalised lm diagram
				enableAll();
				
				$( "#showGrid" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showGrid" ).prop("checked") ){
						plot_options.grid = 1;
					} else { 
						plot_options.grid = 0;
					}
					refreshPlot(plot);
				})
								
				$( "#compare1931-2" ).prop("disabled", true)
				.click(function(){
					
					if ( $( "#compare1931-2" ).prop("checked") ){
						plot_options.cie31 = 1;
					} else { 
						plot_options.cie31 = 0;
					}
					refreshPlot(plot);
				})
				
				$( "#compare1964-10" ).prop("disabled", true)
				.click(function(){
					if ( $( "#compare1964-10" ).prop("checked") ){
						plot_options.cie64 = 1;
					} else { 
						plot_options.cie64 = 0;
					}
					refreshPlot(plot);
				})
				
				
				$( "#showLabels" ).prop("disabled", false)
				.click(function(){
					if ( $( "#showLabels" ).prop("checked") ){
						plot_options.labels = 1;
					} else { 
						plot_options.labels = 0;
					}
					refreshPlot(plot);
				})
			break;
		}
		
	});
	
		$( "#plot-select" ).change(); //Force trigger a change event to initialize checkbox functionality.

});