
// #######################################################
// Select datasets and display correlation guages
// #######################################################

// construct url for endpoint query
var base_url = 'http://dme3x79mz2i5z.cloudfront.net'


// allow only two checkboxes to be selected by keeping track

function keepCount() {
    var NewCount = 0
    
    if (document.select_datasets.violent_crime.checked){
      NewCount = NewCount + 1
      }
    if (document.select_datasets.murder.checked){
      NewCount = NewCount + 1
      }
    if (document.select_datasets.population.checked){
      NewCount = NewCount + 1
      }
    if (document.select_datasets.school_shootings.checked){
      NewCount = NewCount + 1
      }
    if (document.select_datasets.foreclosure.checked){
      NewCount = NewCount + 1
      }
    if (document.select_datasets.snap.checked){
      NewCount = NewCount + 1
      }
    if (NewCount == 3){
      alert('Pick Just Two Please')
      document.select_datasets; return false;
      }
    } 

  // ##########################################
  // Gauge graphs function (creates two)
  // ##########################################
  
  function displayGauges(response){

      // !! REPLACE TWO LINES BELOW WITH PROPER RESPONSE ACCESSORS !!
      // var r = response.r
      // var p = response.p
      // !! BELOW ARE TEST VALUES, REMOVE WHEN ENDPOINT WORKS !!
      var r = 0.48
      var p = 0.03
      
      
      // BELOW IS A MODIFIED VERSION OF THE Plotly.js GAUGE CHART TEMPLATE
      // 2 CHARTS ARE BELOW, ONE FOR R-VALUE, ONE FOR P-VALUE
      
      // ###### FIRST CHART: R-VALUE #####
      
      // Enter a value between -1 and 1
      // For easier trig, modify input variable to be between 0 and 2
      // rather than -1 and 1
      
      var level = r + 1
  
      // Trig to calc meter point
      var degrees = 2 - level,
        radius = .5;
      var radians = degrees * Math.PI / 2;
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
          x: [0], y:[0],
          marker: {size: 28, color:'850000'},
          showlegend: false,
          name: "Pearson's Correlation Coefficient",
          // convert level back to true value for hover by subtracting 1
          text: level - 1,
          hoverinfo: 'text+name'},
        { values: [50/6, 50/6, 50/6, 50/6, 50/6, 50/6, 50],
          rotation: 90,
          text: ['Strong Positive', 'Fair Positive', 'Weak Positive', 'Weak Negative',
                 'Fair Negative', 'Strong Negative', ''],
          textinfo: 'text',
          textposition:'inside',
          marker: {colors:['rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                           'rgba(232, 226, 202, .5)', 'rgba(232, 226, 202, .5)',
                           'rgba(110, 154, 22, .5)', 'rgba(14, 127, 0, .5)',
                           'rgba(255, 255, 255, 0)']},
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
  
      Plotly.newPlot('r_gauge', data, layout);
  
      // ###### SECOND CHART: P-VALUE #####
  
      // Enter a value between 0 and 1
      // As P values above 0.1 are unacceptable, if p is over 0.1, set guage to
      // maximum (0.1). We want to gauge to show values between 0 and 0.1
      
      if (p > 0.1){
          var level = 0.1
      } else {
          var level = p
      }
      
  
      // Trig to calc meter point
      var degrees = 0.1 - level,
        radius = .5;
      var radians = degrees * Math.PI / 0.1;
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
          x: [0], y:[0],
          marker: {size: 28, color:'850000'},
          showlegend: false,
          name: "2-Tailed P-Value",
          text: level,
          hoverinfo: 'text+name'},
        { values: [50/6, 50/6, 50/6, 50/6, 50/6, 50/6, 50],
          rotation: 90,
          text: ['Very High', 'High', 'Questionable', 'Acceptable',
                 'Low', 'Very Low', ''],
          textinfo: 'text',
          textposition:'inside',
          marker: {colors:[
                           'rgba(196, 62, 62, .5)',
                           'rgba(196, 125, 62, .5)',
                           'rgba(196, 167, 62, .5)',
                           'rgba(182, 196, 62, .5)',
                           'rgba(125, 196, 62, .5)',
                           'rgba(62, 196, 100, .5)',
                           'rgba(255, 255, 255, 0)']},
          labels: ['0.083 to 1.000', '0.067 to 0.083', '0.050 to 0.067', '0.033 to 0.050', '0.017 to 0.033', '0.000 to 0.017', ''],
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
          title: "2-Tailed P-Value",
          height: 500,
          width: 500,
          xaxis: {zeroline:false, showticklabels:false,
                  showgrid: false, range: [-1, 1]},
          yaxis: {zeroline:false, showticklabels:false,
                  showgrid: false, range: [-1, 1]}
                    };
  
      Plotly.newPlot('p_gauge', data, layout);

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

  function callAPI(){
    // retrieve DOM elements that are checked
    var array = []
    var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
    
    // iterate through DOM elements to extract name and store in array
    for (var i = 0; i < checkboxes.length; i++) {
      array.push(checkboxes[i].name)
    }
    
    // make sure exactly two boxes were checked (keepCount prevents more than two)
    if (array.length < 2) {
      alert('Pick Two Datasets')
    }
  
    // unpack array
    var dataset1 = array[0]
    var dataset2 = array[1]
  
    // console.log the value extraction
    console.log("Dataset name: \n" + dataset1 + "\nhanded to displayGuage() function")
    console.log("Dataset name: \n" + dataset2 + "\nhanded to displayGuage() function")
    
    // base url is at top of this document
    var url = base_url + "/" + dataset1 + "/" + dataset2
  
    // call API and feed response to graphing functions
    Plotly.d3.json(url, function(error, response){
      if (error) console.warn(error)
      
      displayGauges(response)
      displayLines(response)
      
       })
  
      }