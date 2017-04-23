//map.js displays map and markers. refer to map2.js for displaying of table

var map;
var mapCanvas;


google.load("visualization", "1", {packages: ["corechart"]});


//function to initialise the google map. all javascript functions are called within initMap()
function initMap() {
		
	mapCanvas = document.getElementById("map");
		
	var mapOptions = {
	panControl: true,
	zoomControl: true,
	center: {lat: 53.344083, lng: -6.267015},
	zoom: 13  
	};	
	map = new google.maps.Map(mapCanvas, mapOptions);
	
	//initialise legend on the map
	legendInit();
	
	//function that loops through dublin bikes stations
	showStationMarkers(map);
	
}



function showStationMarkers(map) {
	//get json file passed from flask
	
	
	var jqxhr = $.getJSON($SCRIPT_ROOT + "/stations", function(data) {
	
		stations = data.stations;
	
	//loop through each station in json file
    _.forEach(stations, function(station) {
    	
    	//initialise a marker
    	var marker = new google.maps.Marker({
    		position : {
    		lat : parseFloat(station.latitude),
    		lng : parseFloat(station.longitude)
    		},
    	map : map,
    	//change icon dynamically based on available bike_stands
    	icon : {
    		
    		// change marker icon to bikes
    		url: drawBikeMarker(station.bike_stands,station.available_bikes),
    		scaledSize: new google.maps.Size(20, 20),
    	},
    	optimized: false,
    	title : station.name,
    	station_number : station.number
    	});
    	
    	//change colour of markers depending on bike stands occupancy
    	//changeColorMarkers(station.available_bike_stands,marker);
    	
    	infowindow = new google.maps.InfoWindow();
    	
    	
    	//listening in for a click event: show bike stands occupancy chart
    	google.maps.event.addListener(marker, 'click', function() {
    		
    		//draw statistics table below map
    		drawInfoWindowChart(marker);
    		
    		//display weather on each marker
    		displayWeather(marker,station);
    		
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
			chart_data.addColumn('number', 'number_bike_stands');
			chart_data.addColumn('number', 'number_bikes');
			
			_.forEach(data, function(row){
				
				//each row contains a date, the bike stands occupancy and the bikes availability
				chart_data.addRow([new Date(row[0]), row[1], row[2]]);
				})
				
	      var options = {
	        title: 'Bikes / Bike stands availability 3-day timeframe',
	        width: 1200,
	        height: 300,
	        legend: { position: 'bottom' },
	        
	        hAxis: {
	          title: 'Time of Day'
	        },
	        vAxis: {
	          title: 'Number of bike stands / Bikes'
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


//function to show bike station markers. Red bike between 0 and 33 %, Yellow bike between 33 and 66 %, Green bike between 66 and 100% available bikes in a station
function drawBikeMarker(bike_stands,available_bikes) {
	
	var proportion = available_bikes / bike_stands;
	
	if (proportion < 0.33) {
		
		return "/static/images/red_bike.PNG";
		
	}
	
	else if (proportion > 0.33 && proportion < 0.66) {
		
		return "/static/images/yellow_bike.PNG";
		
	}
	
	else {
		
		return "/static/images/green_bike.PNG";
		
	}
	
	
	
	
}



function displayWeather(marker,station) {
	
	//ajax call to openweather API
    $.ajax({
    	
    	// Math.round() to get the specific longitude and latitude
    	//Personal API key
        url: "http://api.openweathermap.org/data/2.5/weather?lat=" + (Math.round(marker.getPosition().lat()*1000000)/1000000) + "&lon=" + (Math.round(marker.getPosition().lng()*1000000)/1000000) + "&appid=314b7c76899a9afd33ffb8d575363c29",
        dataType: 'jsonp',
        //results contains the json file with all information about weather from API
        success: function(results) {
        	
        	
	      	var content_stat="<div><h1>Station: "+station.number+"</h1>"+"<p>"
	      		+station.address+"</p>"+"<p>Available stands: "+station.available_bike_stands
	      		+"</p>"+"<p>Available bikes: "+station.available_bikes+"</p> <p> <img src='/static/weather/"
	      		+results.weather[0].icon+".png'> </p> <p> Temperature: " 
	      		+ Math.round((results.main.temp - 273.15)) + " Celsius</p> </div>";
	      	
	    	//listening in for a click event: show bike stands occupancy chart
	    	//google.maps.event.addListener(marker, 'click', function() 
			//calling function to draw the table with statistics about marker
			infowindow.setContent(content_stat);
			infowindow.open(marker.getMap(), marker);
        }
    })
}

//initialise red,yellow,green bike legend in google map
//reference: https://developers.google.com/maps/documentation/javascript/adding-a-legend
function legendInit() {
	
    var icons = {
            red_bike: {
              name: '0-33% Available Bikes',
              icon: "/static/images/red_bike.PNG"
            },
            yellow_bike: {
              name: '33-66% Available Bikes',
              icon: "/static/images/yellow_bike.PNG"
            },
            green_bike: {
              name: '66-100% Available Bikes',
              icon: "/static/images/green_bike.PNG"
            }
          };
	
    var legend = document.getElementById('legend');
    
    for (var key in icons) {
      var type = icons[key];
      var name = type.name;
      var icon = type.icon;
      var div = document.createElement('div');
      div.innerHTML = '<img src="' + icon + '"> ' + name;
      legend.appendChild(div);
    }

    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
	
}


