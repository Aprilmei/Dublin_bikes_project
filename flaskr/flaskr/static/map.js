//map.js displays map and markers. refer to map2.js for displaying of table

var map;
var mapCanvas;

google.load("visualization", "1", {packages: ["corechart"]});

function initMap() {
		
	mapCanvas = document.getElementById("map");
		
	var mapOptions = {
	panControl: true,
	zoomControl: true,
	mapTypeControl: true,
	scaleControl: true,
	streetViewControl: true,
	overviewMapControl: true,
	rotateControl: true,
	center: {lat: 53.344083, lng: -6.267015},
	zoom: 13  
	};	
	map = new google.maps.Map(mapCanvas, mapOptions);
	//calling markers function passing map variable
	showStationMarkers(map);
	
}



function showStationMarkers(map) {
	alert("yt");
	var jqxhr = $.getJSON($SCRIPT_ROOT + "/stations", function(data) {
	alert("vv");
	
		stations = data.stations;
		// draw markers
		
    _.forEach(stations, function(station) {
    	console.log(station.name, station.number);

    	var marker = new google.maps.Marker({
    		position : {
    		lat : parseFloat(station.latitude),
    		lng : parseFloat(station.longitude)
    		},
    	map : map,
    	optimized: false,
    	title : station.name,
    	station_number : station.number
    	});
    	
    	google.maps.event.addListener(marker, 'click', function() {
    	   console.log("marker",marker)
 		   alert("clicked a marker");
		   //calling function to draw the table with statistics about marker
    		drawInfoWindowChart(marker);
    		});
    	
    	
    	contentString = '<div id="content"><h1>' + station.name + '</h1></div>' + '<div id="station_availability"></div>';

    })
		
		})
	.fail(function() {
		console.log( "error showStationMarkers" );
	})
}





function drawInfoWindowChart(marker) {
	
	var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number,
			function(data) {
			data = JSON.parse(data.data);
			console.log('data', data);
			
			var chart_data = new google.visualization.DataTable();
			chart_data.addColumn('datetime', 'Time of Day');
			chart_data.addColumn('number', '#');
			_.forEach(data, function(row){
				chart_data.addRow([new Date(row[0]), row[1]]);
				})
				
	      var options = {
	        title: 'Bikes availability today',
	        width: 1200,
	        height: 300,
	        
	        hAxis: {
	          title: 'Time of Day'
	        },
	        vAxis: {
	          title: 'Number of bikes'
	        }
	      };
				
			
			var node = document.getElementById("chart_div");
			var chart = new google.visualization.LineChart(node);


			chart.draw(chart_data,options);

	})
}



	
	 
