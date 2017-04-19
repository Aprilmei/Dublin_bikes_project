//map.js displays map and markers. refer to map2.js for displaying of table

var map;
var mapCanvas;



//google.charts.load('current', {'packages': ['corechart'], 'callback': drawInfoWindowChart});

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
	var map = new google.maps.Map(mapCanvas, mapOptions);
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
    	
    	
    	contentString = '<div id="content"><h1>' + station.name + '</h1></div>' + '<div id="station_availability"></div>';
    	
    	google.maps.event.addListener(marker, 'click', function() {
    		alert("event listener");
    		//calling function to draw column chart in map2.js onclick of a marker
    		drawInfoWindowChart(this);
    		});

    })
		
		})
	.fail(function() {
		console.log( "error showStationMarkers" );
	})
}



	

