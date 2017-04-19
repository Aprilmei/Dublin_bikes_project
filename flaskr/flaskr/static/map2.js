// map2.js displays a table with statistics onclick of one of the markers

var wrapper;

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