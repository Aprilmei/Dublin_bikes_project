//map.js displays map and markers. refer to map2.js for displaying of table

var map;
var mapCanvas;

google.load("visualization", "1", {packages: ["corechart"]});

function initMap() {
		
	mapCanvas = document.getElementById("map");
		
	var mapOptions = {
	panControl: true,
	zoomControl: true,
	center: {lat: 53.344083, lng: -6.267015},
	zoom: 13  
	};	
	map = new google.maps.Map(mapCanvas, mapOptions);
	//calling markers function passing map variable
	showStationMarkers(map);
	
}



function showStationMarkers(map) {
	var jqxhr = $.getJSON($SCRIPT_ROOT + "/stations", function(data) {
	
		stations = data.stations;
		// loading standard green icon, improves speed later on.
		var image_green = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
		var image_red = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
		
		console.log('received station markers');
		console.log("stations", stations);
    _.forEach(stations, function(station) {
    	
    	var marker = new google.maps.Marker({
    		position : {
    		lat : parseFloat(station.latitude),
    		lng : parseFloat(station.longitude)
    		},
    	map : map,
    	//change icon dynamically based on available bike_stands
    	icon : {
    		
    		url: station.available_bike_stands == 0 ? image_red : image_green,
    	},
    	optimized: false,
    	title : station.name,
    	station_number : station.number
    	});
    	
    	//change colour of markers depending on bike stands occupancy
    	//changeColorMarkers(station.available_bike_stands,marker);
    	
    	
    	//listening in for a click event: show bike stands occupancy chart
    	google.maps.event.addListener(marker, 'click', function() {
    		
		   //calling function to draw the table with statistics about marker
    		drawInfoWindowChart(marker);
    		});
    	

    })
		
		})
	.fail(function() {
		console.log( "error showStationMarkers" );
	})
}




// function to draw bike stands occupancy chart below google map
function drawInfoWindowChart(marker) {
	
	var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number,
			function(data) {
			data = JSON.parse(data.data);
			
			//initialising and populating the data table
			var chart_data = new google.visualization.DataTable();
			chart_data.addColumn('datetime', 'Time of Day');
			chart_data.addColumn('number', '#');
			_.forEach(data, function(row){
				//each row contains a date and the bike stands occupancy
				chart_data.addRow([new Date(row[0]), row[1]]);
				})
				
	      var options = {
	        title: 'Bike stands availability today',
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
	.fail(function() {
		console.log( "error drawInfoWindowChart" );
	})
}




