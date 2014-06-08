/* 	Plot loader 
	functions to handle plot loading/updating.
	Author: Gerardo de La Riva, 2014
*/


//Object to store all variants of a plot.
var all_plots = [];
var availablePlots = [ 	'lms', 
						'lms_base', 
						'lm',
						'bm',
						'xy', 
						'xyz',
						'xyz31',
						'xy31' ];
						
function Plot ( name ){
	
	var plot_name = this.name = name;
	var plot_html = this.plot_html = [];
	
	this.setPlot = function(plot_options, plot_data){
		plot_html[plot_options] = plot_data;
	}	
		
	this.getPlot = function(plot_options){
		return plot_html[plot_options];
	}
}

for (i=0; i < availablePlots.length; i++){
	all_plots[availablePlots[i]] = new Plot(availablePlots[i]);

}



