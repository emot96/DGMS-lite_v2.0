/*------------------------------------------JS for "Energy Output" chart ------------------------------------------------*/

var energy_op = document.getElementById('energy_op').getContext('2d');
var myChart = new Chart(energy_op, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'kVA',
            fill: false,
            data: [8, 8, 6, 6, 8, 8, 7 ,15, 8, 8, 8, 8, 8, 8,10],
            borderColor:'rgba(103, 128, 159, 1)',
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
            text: 'Energy Output (kVA)',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Watts total" chart ------------------------------------------------*/

var watts_load = document.getElementById('watts_load').getContext('2d');
var myChart1 = new Chart(watts_load, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'kW',
            fill: false,
            data: [8, 8, 6, 6, 8, 8, 7 ,9, 8, 8, 8, 8, 8, 8,10],
            borderColor:'rgba(246, 71, 71, 1)',
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
            text: 'Energy Output (kW)',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Average Current" chart ------------------------------------------------*/

var avg_cur = document.getElementById('avg_cur').getContext('2d');
var myChart2 = new Chart(avg_cur, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Average Current',
            fill: false,
            data: [8, 8, 6, 6, 8, 8, 7 ,16, 8, 8, 8, 8, 8, 8,10],
            borderColor:'rgba(137, 196, 244, 1)',
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
            text: 'Average Current',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});
       

/*------------------------------------------JS for "Current RBY" chart ------------------------------------------------*/

var cur_rby = document.getElementById('cur_rby').getContext('2d');
var chart9 = new Chart(cur_rby, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00'],
        datasets: [{
            label: 'CurrentPhaseR',
            fill: false,
            data: [11, 2, 11, 2,11, 2, 0],
            borderColor: 'rgba(207, 0, 15, 1)',
            borderWidth: 2
        },
        {
            label: 'CurrentPhaseY',
            fill: false,
            data: [2, 4, 6, 5,5, 2, 1],
            borderColor: 'rgba(247, 202, 24, 1)',
            borderWidth: 2   
        },
        {
            label: 'CurrentPhaseB',
            fill: false,
            data: [10, 6, 6, 2,11, 1, 10],
            borderColor:'rgba(44, 130, 201, 1)',
            borderWidth: 2   
        }
    ]
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
            text: 'Phasewise Curren',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
      }
});
         
