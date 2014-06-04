/* Script to manage tc web app */
$( ).ready(function(){	


//Load the default plots via ajax:
	

var availablePlots = [ 'xyz', 'xy', 'lms', 'lms_base', 'bm', 'lm' ];


//@TODO: Need to asynch this. I will repeat the code for now:

//xyz
			$.get( "/get_plot/" + availablePlots[0])
				.done(function( data ) {
					$( "div#" + availablePlots[0] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[0] + " plot from server" );
				});	

//xyz
			$.get( "/get_plot/" + availablePlots[1])
				.done(function( data ) {
					$( "div#" + availablePlots[1] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[1] + " plot from server" );
				});	

//lms
			$.get( "/get_plot/" + availablePlots[2])
				.done(function( data ) {
					$( "div#" + availablePlots[2] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[2] + " plot from server" );
				});	

// lms_base
			$.get( "/get_plot/" + availablePlots[3])
				.done(function( data ) {
					$( "div#" + availablePlots[3] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[3] + " plot from server" );
				});	

//bm
			$.get( "/get_plot/" + availablePlots[4])
				.done(function( data ) {
					$( "div#" + availablePlots[4] +"_plot" ).append(data);
  				})
  				.fail(function() {
    				alert( "error when getting " + availablePlots[4] + " plot from server" );
				});	

//lm

			$.get( "/get_plot/" + availablePlots[5])
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
		
		var plot = $('option:selected', this).attr('plot');
		
		$( "div.plot" ).hide(); 				//Hide all plots
		$( "div.html_text" ).hide();			//Hide all HTML
		$( "div.table" ).hide();				//Hide all tables
		$( "div#" + plot + "_plot" ).show();	//Show selected plot
		$( "div#" + plot + "_html" ).show();	//Show selected HTML
		$( "div#" + plot + "_table" ).show();	//Show selected table
		
		//Enable or disable checkboxes
		
		switch(plot){
		
			case "xyz":
			
			
			break;
			
			case "xy":
			
			break;
			
			case "lms":
			
			break;
			case "lms_base":
			
			break;
			
			case "bm":
			
			break;
			
			case "lm":
			
			break;
			
		
		}
		
	});


});