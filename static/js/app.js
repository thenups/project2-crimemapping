// Mapbox Token - AMS
mapboxgl.accessToken = 'pk.eyJ1IjoiYW1zb3ciLCJhIjoiY2plbHBoaGQ2MWxnajMzbjV2eWVmam5kdiJ9.jFX6_Ms_zLtF7BDkw12hTw';

// Initiate Map
var map = new mapboxgl.Map({
  container: 'map', // container element id
  style: 'mapbox://styles/mapbox/light-v9',
  center: [-97, 37.5], // initial map center in [lon, lat]
  pitch: 0, // pitch in degrees
  bearing: 0, // bearing in degrees
  zoom: 3
});

// Setting Choropleth Legend //
var layers = ['0-10', '10-20', '20-50', '50-100', '100-200', '200-500', '500-1000', '1000+'];
var colors = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'];

for (i = 0; i < layers.length; i++) {
  var layer = layers[i];
  var color = colors[i];
  var item = document.createElement('div');
  var key = document.createElement('span');
  key.className = 'legend-key';
  key.style.backgroundColor = color;

  var value = document.createElement('span');
  value.innerHTML = layer;
  item.appendChild(key);
  item.appendChild(value);
  legend.appendChild(item);
}

// var years = [
//     '1990',
//     '1991',
//     '1992',
//     '1993',
//     '1994',
//     '1995',
//     '1996',
//     '1997',
//     '1998',
//     '1999',
//     '2000',
//     '2001',
//     '2002'
// ];

// Filter by Year Function //
// function filterBy(year) {
//
//     var filters = ['==', 'YEAR', year];
//     // map.setFilter('crime', filters);
//     map.setFilter('shootings', filters);
//
//     // Set the label to the month
//     document.getElementById('active-year').textContent = years[year];
// };

// Map Console Casualty Scale
map.on('load', function() {

  // d3.json('https://functional-vice.herokuapp.com/api/v1.0/schoolShootings/1995', function(err, data) {
  //   if (err) throw err;
  //
  //   // Create a month property value based on time
  //   // used to filter against.
  //   data.features = data.features.map(function(d) {
  //       d.properties.YEAR = new Year(d.properties.YEAR).getYear();
  //       return d;
  //   });

    //crime rate data endpoint //
    map.addSource('crimeData', {
      type: 'geojson',
      data: 'https://functional-vice.herokuapp.com/api/v1.0/crimeRate/1995'
    });
    // shooting fatalities data endpoint //
    map.addSource('shootData', {
      type: 'geojson',
      data: 'https://functional-vice.herokuapp.com/api/v1.0/schoolShootings/1995'
    });

  // choropleth layer
    map.addLayer({
      id: 'crime',
      type: 'fill',
      source: 'crimeData',
      paint: {
        'fill-color': [
            'interpolate',
            ['linear'],
            ['get', 'VCR'],
            0, '#FFEDA0',
            25, '#FED976',
            50, '#FEB24C',
            100, '#FD8D3C',
            200, '#FC4E2A',
            500, '#E31A1C',
            1000, '#BD0026',
        ],
        'fill-opacity': 0.7
      }
    }, 'admin-2-boundaries-dispute');

    // Add Shooting Points Layers //
    map.addLayer({
      id: 'shootings',
      type: 'circle',
      source: 'shootData',
      paint: {
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['number', ['get', 'FATALITIES']],
          0, 10,
          25, 50
        ],
        'circle-color': [
          'interpolate',
          ['linear'],
          ['number', ['get', 'FATALITIES']],
          0, '#2DC4B2',
          1, '#3BB3C3',
          2, '#669EC4',
          3, '#8B88B6',
          4, '#A2719B',
          5, '#AA5E79'
        ],
        'circle-opacity': 0.8
      }
    }, 'admin-2-boundaries-dispute');

  // Toggle Map Layers //
    var toggleableLayerIds = [ 'crime', 'shootings' ];

    for (var i = 0; i < toggleableLayerIds.length; i++) {
        var id = toggleableLayerIds[i];

        var link = document.createElement('a');
        link.href = '#';
        link.className = 'active';
        link.textContent = id;

        link.onclick = function (e) {
            var clickedLayer = this.textContent;
            e.preventDefault();
            e.stopPropagation();

            var visibility = map.getLayoutProperty(clickedLayer, 'visibility');

            if (visibility === 'visible') {
                map.setLayoutProperty(clickedLayer, 'visibility', 'none');
                this.className = '';
            } else {
                this.className = 'active';
                map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
            }
        };

        var layers = document.getElementById('menu');
        layers.appendChild(link);
    }

    // On Mouse hover over states, Show in stats container //
    map.on('mousemove', function(e) {
      var crime = map.queryRenderedFeatures(e.point, {
        layers: ['crime']
      });
      var shootings = map.queryRenderedFeatures(e.point, {
        layers: ['shootings']
      });

      if (shootings.length > 0) {
        document.getElementById('pd').innerHTML = '<h4><strong>' + shootings[0].properties.CITY + ', ' + shootings[0].properties.STATE + '</h4></strong>' + 'Year: ' + shootings[0].properties.YEAR + '<p>Fatalities: ' + shootings[0].properties.FATALITIES + '</p>' ;
        } else if (crime.length > 0) {
          document.getElementById('pd').innerHTML = '<h4><strong>' + crime[0].properties.STATE + '</h4></strong>' + 'Year: ' + crime[0].properties.YEAR + '<p>Violent Crime Rate: ' + crime[0].properties.VCR + '</p>' ;
        } else {
          document.getElementById('pd').innerHTML = '<p>Hover over a state!</p>';
        }
    });

    // Filter Through Years //
    document.getElementById('slider').addEventListener('input', function(e) {
      var year = parseInt(e.target.value);
      // update the map
      map.setFilter('shootings', ['==', ['number', ['get', 'YEAR']], year]);
      map.setFilter('crime', ['==', ['number', ['get', 'YEAR']], year]);

      document.getElementById('active-year').innerText = year;
      
    });

    // Setting default filter value //
    // filterBy(0);
    //
    // // wait for user input, run function filterBy //
    // document.getElementById('slider').addEventListener('input', function(e) {
    //     var year = parseInt(e.target.value, 10);
  //   //     filterBy(year);
  // });
});


// // Time slider
// document.getElementById('slider').addEventListener('input', function(e) {
//   var hour = parseInt(e.target.value);
//   // update the map
//   map.setFilter('shootings', ['==', ['number', ['get', 'YEAR']], year]);
//
//   document.getElementById('active-year').innerText = year;
//
//   // converting 0-23 hour to AMPM format
//   var ampm = hour >= 12 ? 'PM' : 'AM';
//   var hour12 = hour % 12 ? hour % 12 : 12;
//   // update text in the UI
//   document.getElementById('active-hour').innerText = hour12 + ampm;



// Map/Layer Filter
// document.getElementById('filters').addEventListener('change', function(e) {
//   var day = e.target.value;
//   // update the map filter
//   if (day === 'all') {
//     filterDay = ['!=', ['string', ['get', 'YEAR']], 'placeholder'];
//   } else if (day === 'weekday') {
//     filterDay = ['match', ['get', 'Day'], ['Sat', 'Sun'], false, true];
//   } else if (day === 'weekend') {
//     filterDay = ['match', ['get', 'Day'], ['Sat', 'Sun'], true, true];
//   } else {
//     console.log('error');
//   }
//   map.setFilter('crimeRate', ['all', filterDay]);
// });

// Confirming version of active js file
console.log('hello 2.18');
