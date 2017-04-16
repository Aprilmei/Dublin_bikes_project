var map;
var mapCanvas;

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
	//calling markers functio paasing map variable
	showStationMarkers(map);
}



function showStationMarkers( map) {
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
    	title : station.name,
    	station_number : station.number
    	});
    })
		
		})
	.fail(function() {
		console.log( "error" );
	})
}