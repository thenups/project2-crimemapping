// #######################################################
// Select datasets and display correlation guages
// #######################################################

// construct url for endpoint query
// var baseURL = 'http://dme3x79mz2i5z.cloudfront.net/api/v1.0/national/sum/'
var baseURL = 'https://functional-vice.herokuapp.com/api/v1.0/national/sum/'

// Array for order of selection
var order = [];

// Whenever a new checkbox is clicked, make sure only 2 are selected and change the choice otherwise
$("[type=checkbox]").on('change', function() { // always use change event

    // If someone is clicking on a 3rd selection
    if ($('input[type=checkbox]:checked').length > 2) {
        // uncheck the first box
        $(order[0]).prop('checked', false);

        order.shift(); // remove 1st element
        order.push(this); // add newly selected

        console.log(order);
    }

    // check for index number
    var idx = order.indexOf(this);

    if (idx !== -1) {         // if already in array
    	order.splice(idx, 1); // make sure we remove it
    }

    if (this.checked) {    // if checked
    	order.push(this);  // add to end of array
    }

    // Don't allow user to select button unless there are two selections
    if (order.length < 2){
        $('#correlateBtn').attr("disabled", true);
    } else {
        $('#correlateBtn').attr("disabled", false);
    }
});


function callAPI(){
    // retrieve DOM elements that are checked
    var array = [];

    // iterate through DOM elements to extract name and store in array
    for (var i = 0; i < order.length; i++) {
        array.push(order[i].value);
    };

    // unpack array
    var dataset1 = array[0];
    var dataset2 = array[1];

    // console.log the value extraction
    console.log("Dataset name: \n" + dataset1 + "\nhanded to displayGuage() function");
    console.log("Dataset name: \n" + dataset2 + "\nhanded to displayGuage() function");

    // base url is at top of this document
    var apiCall = baseURL + dataset1 + '/' + dataset2;
    console.log(apiCall);

    // call API and feed response to graphing functions
    Plotly.d3.json(apiCall, function(error, response){
        if (error) console.warn(error);

        displayR(response);
        // displayP(response);
        // displayLines(response);
    });
};


// ##########################################
// Gauge graphs function (creates two)
// ##########################################

function displayR(response){

    // !! REPLACE TWO LINES BELOW WITH PROPER RESPONSE ACCESSORS !!
    var r = response['r-value']
    var p = response['p-value']

    console.log(r);
    console.log(p);


    // BELOW IS A MODIFIED VERSION OF THE Plotly.js GAUGE CHART TEMPLATE
    // 2 CHARTS ARE BELOW, ONE FOR R-VALUE, ONE FOR P-VALUE

    // ###### FIRST CHART: R-VALUE #####

    // Enter a value between -1 and 1
    // For easier trig, modify input variable to be between 0 and 2
    // rather than -1 and 1
    // check if correlation is positive or negative and adjust level

    var level = r + 1

    // Trig to calc meter point
    var degrees = 180 - (level*90),
    radius = .5;
    var radians = degrees * Math.PI / 180;
    var x = radius * Math.cos(radians);
    var y = radius * Math.sin(radians);

  // Path: may have to change to create a better triangle
    var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
        pathX = String(x),
        space = ' ',
        pathY = String(y),
        pathEnd = ' Z';
    var path = mainPath.concat(pathX,space,pathY,pathEnd);

    var data = [{ type: 'scatter',
        x:[0], y:[0],
        marker: {size: 28, color:'850000'},
        showlegend: false,
        name: "Pearson's Correlation Coefficient",
        // convert level back to true value for hover by subtracting 1
        text: level - 1,
        hoverinfo: 'text'},
        { values: [50/6, 50/6, 50/6, 50/6, 50/6, 50/6, 50],
        rotation: 90,
        text: ['Strong Positive', 'Fair Positive', 'Weak Positive', 'Weak Negative',
             'Fair Negative', 'Strong Negative', ''],
        textinfo: 'text',
        textposition:'inside',
        marker: {colors:[
            'rgba(27,120,55,.75)',
            'rgba(127,191,123,.75)',
            'rgba(217,240,211,.5)',
            'rgba(209,229,240,.75)',
            'rgba(103,169,207,.75)',
            'rgba(33,102,172,.75)',
            'rgba(255,255,255,0)']},
        labels: ['0.6 to 1.0', '0.3 to 0.6', '0.0 to 0.3', '-0.3 to 0.0', '-0.6 to -0.3', '-1.0 to -0.6', ''],
        hoverinfo: 'label',
        hole: .5,
        type: 'pie',
        showlegend: false
    }];

    var layout = {
        shapes:[{
                  type: 'path',
                  path: path,
                  fillcolor: '850000',
                  line: {
                          color: '850000'
                        }
                }],
        title: "Pearson's Correlation Coefficient",
        height: 500,
        width: 500,
        xaxis: {zeroline:false, showticklabels:false,
              showgrid: false, range: [-1, 1]},
        yaxis: {zeroline:false, showticklabels:false,
              showgrid: false, range: [-1, 1]}
                };

    Plotly.newPlot('rGauge', data, layout);

}


  // ###########################################
  // Line Graph Function
  // ###########################################

  function displayLines(response){

          // !! CHANGE ACCESSORS TO FIT JSON !!
          //var first_array = response.dataset1.value_array
          //var second_array = response.dataset2.value_array
          //var dataset1_name = reponse.dataset1.name
          //var dataset2_name = response.dataset2.name
          var year_array = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]

          // TEST VALUES:
          var first_array = [1,2,3,4,5,6,7,8,9,10,11]
          var second_array = [21,22,23,24,25,26,27,28,29,30,31]
          var dataset1_name = "violent_crime"
          var dataset2_name = "snap"

          // Below is modified Plotly stacked line chart template
          var trace1 = {
            x: year_array,
            y: first_array,
            name: dataset1_name,
            type: 'scatter'
          };

          var trace2 = {
            x: year_array,
            y: second_array,
            name: dataset2_name,
            xaxis: 'x2',
            yaxis: 'y2',
            type: 'scatter'
          };

          var data = [trace1, trace2];

          var layout = {
            title: (dataset1_name + " and " + dataset2_name + " 2004-2014"),
            yaxis: {domain: [0, 0.45]},
            legend: {traceorder: 'reversed'},
            xaxis2: {anchor: 'y2',
                     title: 'Year'},
            yaxis2: {domain: [0.55, 1]}
          };

          Plotly.newPlot('stacked_line', data, layout);

  }



  // ###################################################
  // Retrieve checkbox selections and call API function
  // ###################################################

  // when check correlation button is clicked, below function is run
  // to extract name property of checked checkboxes and call api,
  // response is fed to the two graphing functions, which parse
  // the pieces of the response they require
