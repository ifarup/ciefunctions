/* Script to manage tc web app */

$( ).ready(function(){

//Initialization of jQuery UI tabs

	$( "#tc-Tabs" ).tabs({
					heightStyle: "content",
					});

//@TODO: Need to make navigation buttons (home, magnifier, cross) more visible.
	$( "image" ).css("opacity", 1); //To make the nav elements more visible.


//Start by showing XYZ plot + data:

	$( "#xyz_plot" ).show();
	$( "#xyz_html" ).show();


//Changing plots:

	$( "select#plot-select" ).on("change", function(){
		
		var plot = $('option:selected', this).attr('plot');
		
		$( "div.plot" ).hide(); 				//Hide all plots
		$( "div.html_text" ).hide();			//Hide all HTML
		$( "div#" + plot + "_plot" ).show();	//Show selected plot
		$( "div#" + plot + "_html" ).show();	//Show selected HTML
	});


});