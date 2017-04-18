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
	//calling markers functio paasing map variable
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
    		drawInfoWindowChart(this);
    		});

    })
		
		})
	.fail(function() {
		console.log( "error" );
	})
}


function drawInfoWindowChart(marker) {
	
	alert("drawinfowindowchart");
	var jqxhrt = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number, function(data) {
		alert("inside");
		data = JSON.parse(data.data);
		console.log('data', data);
		var node = document.getElementById('chart_div');
		var infowindow = new google.maps.InfoWindow();
		var chart = new google.visualization.ColumnChart(node);
		console.log('node',node)
		var chart_data = new google.visualization.DataTable();
		chart_data.addColumn('datetime', 'Time of Day');
		chart_data.addColumn('number', '#');
		
		_.forEach(data, function(row){
			chart_data.addRow([new Date(row[0]), row[1]]);
		})
		
		chart.draw(chart_data, options);
		infowindow.setContent(node);
		infowindow.open(marker.getMap(), marker);
	})
	
	.fail(function() {
			console.log( "error" );
	})
				
	
}
	

