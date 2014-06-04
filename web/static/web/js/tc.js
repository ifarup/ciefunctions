/* Script to manage tc web app */

$( ).ready(function(){

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