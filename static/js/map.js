//var baseURL = 'http://dme3x79mz2i5z.cloudfront.net'
var baseURL = 'https://functional-vice.herokuapp.com'

// set defaults for which layer and property hover is looking for
// so it doesn't throw error (it looks for a selected layer on load).
// Gets reset as soon as a toggle is clicked.
currentpropertykey = 'MURDER'
currentlayerid = 'Murders'

function initiateMap(){

  // Mapbox Token - AMS
  mapboxgl.accessToken = 'pk.eyJ1IjoiYW1zb3ciLCJhIjoiY2plbHBoaGQ2MWxnajMzbjV2eWVmam5kdiJ9.jFX6_Ms_zLtF7BDkw12hTw';

  // Initiate Map
    map = new mapboxgl.Map({
    container: 'map', // container element id
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-97, 37.5], // initial map center in [lon, lat]
    pitch: 0, // pitch in degrees
    bearing: 0, // bearing in degrees
    zoom: 3
});

}


// embeded in createChoroplethToggle, this function creates a toggle
// button and links it with the visibility of a layer,
// creation of a custom legend for the displayed layer,
// as well as setting the property the hover function is reading from
function addToggle(layerid, legend_ranges, layerid, propertykey, color_list){

  var id = layerid;

  var link = document.createElement('a');
  link.href = '#';
  link.className = 'inactive';
  link.textContent = id;

  link.onclick = function (e) {
      var clickedLayer = this.textContent;
      e.preventDefault();
      e.stopPropagation();
      // var onbuttons = document.getElementsByClassName('active')
      // for (var i=0; i < onbuttons.length; i++){
      //   var button = onbuttons[i]
      //   button.setAttribute('class', 'inactive')
      // }



      var visibility = map.getLayoutProperty(clickedLayer, 'visibility');

      if (visibility === 'visible') {
          map.setLayoutProperty(clickedLayer, 'visibility', 'none');
          this.className = '';
          // remove legend
          legend.innerHTML = '';
      } else {
          this.className = 'active';
          map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
          // write legend
          legend.innerHTML = '';
          setChoroplethLegend(legend_ranges, color_list)
          // set current visible layer property accessor for hover function
          currentlayerid = layerid
          currentpropertykey = propertykey

      }
  };

  var layers = document.getElementById('menu');
  layers.appendChild(link);

}


function setChoroplethLegend(layer_rangelist, color_list){

  if (layer_rangelist){
    var rangelist = layer_rangelist;
    var colors = color_list;

    for (i = 0; i < rangelist.length; i++) {
      var range = rangelist[i];
      var color = colors[i];
      var item = document.createElement('div');
      var key = document.createElement('span');
      key.className = 'legend-key';
      key.style.backgroundColor = color;

      var value = document.createElement('span');
      value.innerHTML = range;
      item.appendChild(key);
      item.appendChild(value);
      legend.appendChild(item);
    }
  }
}

function addChoroplethToggle(sourcename, defaultyear, layerid, propertykey, stopmarker_list, color_list, legend_ranges){
  //crime rate data endpoint //
  map.addSource(sourcename, {
    type: 'geojson',
    data: baseURL + '/api/v1.0/crime/' + defaultyear
  });

  // choropleth layer
  map.addLayer({
    id: layerid,
    type: 'fill',
    source: sourcename,
    paint: {
      'fill-color': [
          'interpolate',
          ['linear'],
          ['get', propertykey],
          stopmarker_list[0], color_list[0],
          stopmarker_list[1], color_list[1],
          stopmarker_list[2], color_list[2],
          stopmarker_list[3], color_list[3],
          stopmarker_list[4], color_list[4],
          stopmarker_list[5], color_list[5],
          stopmarker_list[6], color_list[6],
      ],
      'fill-opacity': 0.7
    },
    layout: {visibility: "none"}
  }, 'admin-2-boundaries-dispute');

  addToggle(layerid, legend_ranges, layerid, propertykey, color_list)


}

function addShootingsToggle(){
  // shooting fatalities data endpoint //
  map.addSource('shootData', {
    type: 'geojson',
    data: baseURL + '/api/v1.0/schoolShootings/1995'
  });

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

  //addToggle('shootings')

}



initiateMap()

// Map Console Casualty Scale
map.on('load', function() {
    // add choropleth layers
    // all choropleth layers that are added must also be added to slider function (the sourcename, [first argument in addChoroplethToggle])
    addChoroplethToggle('violentcrimeData',
                         1995,
                        'Violent Crimes',
                        'VIOLENT_CRIME',
                        [0,10000,20000,30000,40000,50000,100000],
                        ['#B557FF', '#A049EE', '#8B3BDE', '#762ECE', '#6120BE', '#4C12AE', '#38059E'],
                        ['0-10 Thousand', '10-20 Thousand', '20-30 Thousand', '30-40 Thousand', '40-50 Thousand', '50-60 Thousand', '60+ Thousand']
                      )
    addChoroplethToggle('murderData',
                        1995,
                        'Murders',
                        'MURDER',
                        [0,25,50,100,200,500,1000],
                        ['#FB9441', '#EC7B3C', '#DE6338', '#D04B33', '#C1332F', '#B31B2A', '#A50326'],
                        ['0-10', '10-20', '20-50', '50-100', '100-200', '200-500', '500+'])
    addChoroplethToggle('populationData',
                        1995,
                        'Population',
                        'POPULATION',
                        [0,2000000,4000000,6000000,8000000,10000000,12000000],
                        ['#5DD600', '#53C200', '#49AF00', '#409B00', '#368800', '#2C7400', '#236100'],
                        ['0-2 Million', '2-4 Million', '4-6 Million', '6-8 Million', '8-10 Million', '10-12 Million', '12+ Million'])
    addChoroplethToggle('unemploymentData',
                        1995,
                        'Unemployment',
                        'UNEMPLOYMENT',
                        [0,1,2,3,4,5,6],
                        ['#7AA1FF', '#4658AE', '#5174CA', '#3D5EB0', '#284795', '#14317B', '#001B61'],
                        ['0-2%', '2-4%', '4-6%', '6-8%', '8-10%', '10-12%', '14+'])
    addChoroplethToggle('vcrData',
                        1995,
                        'Violent Crime Rate', 
                        'VCR', [0,100,200,300,400,500,600],
                        ['#B557FF', '#A049EE', '#8B3BDE', '#762ECE', '#6120BE', '#4C12AE', '#38059E'],
                        ['0-100', '100-200', '200-300', '300-400', '400-500', '500-600', '600+'])



    addShootingsToggle()

    // On Mouse hover over states, Show in stats container //
    map.on('mousemove', function(e) {
      var visible_choropleth = map.queryRenderedFeatures(e.point, {
        layers: [currentlayerid]
        //layers: ['crime']
      });
      var shootings = map.queryRenderedFeatures(e.point, {
        layers: ['shootings']
      });

      if (shootings.length > 0) {
        document.getElementById('pd').innerHTML = '<h4><strong>' + shootings[0].properties.CITY + ', ' + shootings[0].properties.STATE + '</h4></strong>' + 'Year: ' + shootings[0].properties.YEAR + '<p>Fatalities: ' + shootings[0].properties.FATALITIES + '</p>' ;
        } else if (visible_choropleth.length > 0) {
          document.getElementById('pd').innerHTML = '<h4><strong>' + visible_choropleth[0].properties.STATE + '</h4></strong>' + 'Year: ' + visible_choropleth[0].properties.YEAR + '<p>' + currentlayerid + ': '  + visible_choropleth[0].properties[currentpropertykey] + '</p>' ;
        } else {
          document.getElementById('pd').innerHTML = '<p>Hover over a state!</p>';
        }
    });



    // Filter Through Years //
    document.getElementById('slider').addEventListener('input', function(e) {
      var year = parseInt(e.target.value);

      // update the slider readout
      document.getElementById('active-year').innerText = year;

      map.getSource('shootData').setData(baseURL + '/api/v1.0/schoolShootings/' + year);
      map.getSource('violentcrimeData').setData(baseURL + '/api/v1.0/crime/' + year);
      map.getSource('murderData').setData(baseURL + '/api/v1.0/crime/' + year);
      map.getSource('populationData').setData(baseURL + '/api/v1.0/crime/' + year);
      map.getSource('unemploymentData').setData(baseURL + '/api/v1.0/crime/' + year);
      map.getSource('vcrData').setData(baseURL + '/api/v1.0/crime/' + year);
    });

});

// Confirming version of active js file
console.log('hello 3.02');
