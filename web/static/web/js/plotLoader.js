/* 	Plot loader 
	functions to handle plot loading/updating.
	Author: Gerardo de La Riva, 2014
*/

//Object to store all variants of a plot.
var all_plots = [];

var availablePlots = [ 	'lms',
						'lms_base',
						'bm',
						'lm',
						'xyz',
						'xy',
						'xyz_purples',
						'xy_purples',
						'xyz31',
						'xy31',
					    'xyz64',
    					'xy64',
];
						
function Plot ( name ){
	var plot_name = this.name = name;
	var plot_html = this.plot_html = [];
	
	this.setPlot = function(plot_options, plot_data){
		plot_html[plot_options] = plot_data;
	};
		
	this.getPlot = function(plot_options){
		return plot_html[plot_options];
	};
}

function flushCache(){
	for (i=0; i < availablePlots.length; i++){
		all_plots[availablePlots[i]] = new Plot(availablePlots[i]);
	}
	console.log("Cache flushed");
}

for (i=0; i < availablePlots.length; i++){
	all_plots[availablePlots[i]] = new Plot(availablePlots[i]);
}

/* @TODO: Adjust position of ordinate label.*/

$( document ).ready(function(){
	/*var leftPos = -170;
	$( ".y_label" ).css("left", leftPos); //Place the label at a distance from the middle of the containing div of the plot.*/
	$( "#tabSys" ).width(620);
});

$( window ).resize(function() {
	//Adjust ordinate label position
	var instantLeft = $( "#theFig" ).width() /2 - 479;
	//console.log(instantLeft);
	$( ".y_label" ).css("left", instantLeft); //Place the label at a distance from the middle of the containing div of the plot.
});


