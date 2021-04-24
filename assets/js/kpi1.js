

/*------------------------------------------JS for "Unit Generated" chart ------------------------------------------------*/

var run_count = document.getElementById('unit_gen').getContext('2d');
var myChart1 = new Chart(unit_gen, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Unit Generated',
            fill:false,
            data: [8, 8, 3, 8, 8, 8, 7 ,8, 8, 12, 8, 8, 8, 8,10],
            borderColor: 'rgba(129, 207, 224, 1)',
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
            text: 'Unit Generated',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Run count" chart ------------------------------------------------*/

var run_count = document.getElementById('run_count').getContext('2d');
var myChart2 = new Chart(run_count, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Run Count',
            fill: false,
            data: [3, 3, 3, 3, 3, 8, 8 ,8, 8, 8, 8, 8, 8, 8,10],
            borderColor: 'rgba(242, 120, 75, 1)',
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
                    fontColor: "balck",
                    beginAtZero: true,
                    fontSize: 17
                }
            }],

            xAxes: [{
                gridLines: {
                    color: "rgba(0,0,0,0)",
                },
                ticks: {
                    fontColor: "balck",
                    fontSize: 17
                }
            }]
        },

        title: {
            display: true,
            text: 'Run Count',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});






/*------------------------------------------JS for "VLN Average" chart ------------------------------------------------*/

var vln_avg = document.getElementById('vln_avg').getContext('2d');
var myChart3 = new Chart(vln_avg, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'VLN Average',
            fill: false,
            data: [8, 8, 8, 8, 8, 8, 4 ,6, 5, 8, 8, 8, 8, 8,10],
            borderColor:'rgba(30, 130, 76, 1)',
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
            text: 'VLN Average',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});

/*------------------------------------------JS for "Average Voltage VLL" chart ------------------------------------------------*/

var avg_voltage = document.getElementById('avg_voltage').getContext('2d');
var myChart4 = new Chart(avg_voltage, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'VLL',
            fill: false,
            data: [8, 8, 6, 7, 8, 9, 10 ,8, 8, 8, 8, 8, 8, 8,10],
            borderColor: 'rgba(247, 202, 24, 1)',
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
            text: 'VLL',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }

    }
});    

/*------------------------------------------JS for "Frequency" chart ------------------------------------------------*/

var cfreq = document.getElementById('freq').getContext('2d');
var myChart5 = new Chart(freq, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Frequency',
            fill: false,
            data: [8, 8, 5, 20, 8, 8, 8 ,8, 8, 8, 8, 8, 8, 8,10],
            borderColor: 'rgba(210, 82, 127, 1)',
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
            text: 'Frequency',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }

    }
});  


