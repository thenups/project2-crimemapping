// #######################################################
// Select datasets and display correlation guages
// #######################################################
// construct url for endpoint query
// var baseURL = 'http://dme3x79mz2i5z.cloudfront.net/api/v1.0/national/'
var baseURL = 'https://functional-vice.herokuapp.com/api/v1.0/national/'

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



var valueToName = {
    'violent_crime' : 'Violent Crime',
    'murder' : 'Murder',
    'population':'Population',
    'foreclosure':'Foreclosure',
    'snap': 'Food Stamp Participation'
}

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
        displayP(response);
        displayLines(response);
        document.getElementById('graphs').style.display = 'inline';
    });
};


// ##########################################
// Gauge graphs function
// ##########################################

function displayR(response){

    var r = response['r-value']

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

    // Calculate size
    // var parentWidth = document.getElementById("gaugeGraph").offsetWidth,
    //     parentHeight = document.getElementById("gaugeGraph").offsetHeight;

    var data = [{ type: 'scatter',
        x:[0], y:[0],
        marker: {size: 28, color:'850000'},
        showlegend: false,
        // name: "Pearson's Correlation Coefficient",
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
        title: "Pearson's Correlation Coefficient (R-Value)",
        height: 450,
        width: 760,
        xaxis: {zeroline:false, showticklabels:false,
              showgrid: true, range: [-1, 1]},
        yaxis: {zeroline:false, showticklabels:false,
              showgrid: true, range: [-1, 1]}
                };

    Plotly.newPlot('rGauge', data, layout);

}


// ##########################################
// Populate P-value (creates two)
// ##########################################

function displayP(response){
    $('#pSelectedImage').remove();

    var p = response['p-value'];
    var filePath = '../static/images/pvalue/';

    var images = {
        'good': 'good.jpg',
        'bad': 'bad.jpg',
        'ugly': 'ugly.jpg',
        'woah': 'woah.png',
        'duh': 'duh.jpg'
    };

    if (p>0.25) {
        var status = 'ugly';
    } else if (p>0.05) {
        var status = 'bad';
    } else if (p>0.0003) {
        var status = 'good';
    } else if (p<0.000001) {
        var status = 'duh';
    } else {
        var status = 'woah'
    };

    var imagePath = filePath+images[status];


    $('#pValue').text(p.toFixed(7));

    $('#pImg').prepend($('<img>',{
        id:'pSelectedImage',
        src:imagePath,
        class:'img-fluid'
    }));
}

// ###########################################
// Line Graph Function
// ###########################################

function displayLines(response){

    // Get keys from response
    var datasets = Object.keys(response)
    console.log(datasets);
    // Remove P and R value
    var iR = datasets.indexOf('r-value');
    var iP = datasets.indexOf('p-value');
    datasets.splice( iR, 1 );
    datasets.splice( iP, 1 );


    // !! CHANGE ACCESSORS TO FIT JSON !!
    var array1 = response[datasets[0]]
    var array2 = response[datasets[1]]
    var dataset1Name = datasets[0]
    var dataset2Name = datasets[1]
    var yearArray = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]

    console.log('array1',array1);
    console.log('dataset name',dataset1Name);

    console.log('array2',array2);
    console.log('dataset name',dataset2Name);

    // TEST VALUES:
    // var first_array = [1,2,3,4,5,6,7,8,9,10,11]
    // var second_array = [21,22,23,24,25,26,27,28,29,30,31]
    // var dataset1_name = "violent_crime"
    // var dataset2_name = "snap"

    // Below is modified Plotly stacked line chart template
    var trace1 = {
        x: yearArray,
        y: array1,
        name: valueToName[dataset1Name],
        type: 'scatter'
    };

    var trace2 = {
        x: yearArray,
        y: array2,
        name: valueToName[dataset2Name],
        yaxis: 'y2',
        type: 'scatter'
    };

    var data = [trace1, trace2];

    var layout = {
        title: (valueToName[dataset1Name] + " and " + valueToName[dataset2Name] + " 2004-2014"),
        xaxis: {title: 'Year'},
        yaxis: {title: valueToName[dataset1Name]},
        yaxis2: {title: valueToName[dataset2Name],
                 overlaying: 'y',
                 side: 'right'},
        legend: {showlegend: true,
                 "orientation": "h",
                 x: 0,
                 y: 1.15
                },
    };

    Plotly.newPlot('lineGraph', data, layout);

}



  // ###################################################
  // Retrieve checkbox selections and call API function
  // ###################################################

  // when check correlation button is clicked, below function is run
  // to extract name property of checked checkboxes and call api,
  // response is fed to the two graphing functions, which parse
  // the pieces of the response they require
