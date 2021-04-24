/*------------------------------------------JS for "Run Hour" chart ------------------------------------------------*/

// var run_count = document.getElementById('run_hr').getContext('2d');
// var myChart = new Chart(run_hr, {
//     type: 'bar',
//     data: {
//         labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
//         datasets: [{
//             label: 'Run Hour',
//             fill: false,
//             data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
//             backgroundColor: 'rgba(242, 38, 19, 0.4)',
//             borderColor: 'rgba(242, 38, 19, 0.5)',
//             borderWidth: 2
//         },
//         {
//             type: 'line',
//             label: 'Run Hour',
//             fill: false,
//             data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
//             borderColor: 'rgba(242, 38, 19, 1)',
//             borderWidth: 2
//         }]
//     },
//     options: {
      
//       legend: {
//                 labels: {
//                     fontColor: "black",
//                     fontSize: 13
//                 }
//             },

//         scales: {
//             yAxes: [{
//                 gridLines: {
//                     color: "rgba(0,0,0,0.3)",
//                 },
//                 ticks: {
//                     fontColor: "black",
//                     beginAtZero: true,
//                     fontSize: 17
//                 }
//             }],

//             xAxes: [{
//                 gridLines: {
//                     color: "rgba(0,0,0,0)",
//                 },
//                 ticks: {
//                     fontColor: "black",
//                     fontSize: 17
//                 }
//             }]
//         },

//         title: {
//             display: true,
//             text: 'Run Hour',
//             fontSize: 17,
//             fontColor: "balck",
//             fontFamily: "Helvetica"
//         }
//     }
// });

/*------------------------------------------JS for "Load eff" chart ------------------------------------------------*/

var load_eff = document.getElementById('load_ef').getContext('2d');
var myChart = new Chart(load_eff, {
    type: 'bar',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Load Efficiency',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            backgroundColor: 'rgba(42, 187, 155, 0.4)',
            borderColor: 'rgba(42, 187, 155, 0.5)',
            borderWidth: 2
        },
        {
            type: 'line',
            label: 'Load Efficiency',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            borderColor: 'rgba(42, 187, 155, 1)',
            borderWidth: 2
        }]
    },
    options: {
      
      legend: {
                labels: {
                    fontColor: "black",
                    fontSize: 13
                }
            },

        scales: {
            yAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0.3)",
                },
                ticks: {
                    fontColor: "black",
                    beginAtZero: true,
                    fontSize: 17
                }
            }],

            xAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0)",
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 17
                }
            }]
        },

        title: {
            display: true,
            text: 'Load Efficiency',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Peak Load chart ------------------------------------------------*/

var peak_load = document.getElementById('peak_load').getContext('2d');
var myChart = new Chart(peak_load, {
    type: 'bar',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Peak Load',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            backgroundColor: 'rgba(241, 130, 141,0.4)',
            borderColor: 'rgba(241, 130, 141,0.5)',
            borderWidth: 2
        },
        {
            type: 'line',
            label: 'Peak Load',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            borderColor: 'rgba(241, 130, 141,1)',
            borderWidth: 2
        }]
    },
    options: {
      
      legend: {
                labels: {
                    fontColor: "black",
                    fontSize: 13
                }
            },

        scales: {
            yAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0.3)",
                },
                ticks: {
                    fontColor: "black",
                    beginAtZero: true,
                    fontSize: 17
                }
            }],

            xAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0)",
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 17
                }
            }]
        },

        title: {
            display: true,
            text: 'Peak Load',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});



/*------------------------------------------JS for "Carbon Footprint" chart ------------------------------------------------*/

var carbon= document.getElementById('carbon').getContext('2d');
var myChart = new Chart(carbon, {
    type: 'bar',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Carbon Footprint',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            backgroundColor: 'rgba(46, 204, 113, 0.4)',
            borderColor: 'rgba(46, 204, 113, 0.5)',
            borderWidth: 2
        },
        {
            type: 'line',
            label: 'Carbon Footprint',
            fill: false,
            data: [8, 4, 8, 6, 8, 7, 9 ,3, 1, 8, 6, 5, 8, 8,10],
            borderColor: 'rgba(46, 204, 113, 1)',
            borderWidth: 2
        }]
    },
    options: {
      
      legend: {
                labels: {
                    fontColor: "black",
                    fontSize: 13
                }
            },

        scales: {
            yAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0.3)",
                },
                ticks: {
                    fontColor: "black",
                    beginAtZero: true,
                    fontSize: 17
                }
            }],

            xAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0)",
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 17
                }
            }]
        },

        title: {
            display: true,
            text: 'Carbon Footprint',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});





