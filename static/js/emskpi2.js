/*------------------------------------------JS for "Peak Load" chart ------------------------------------------------*/

var peak_ld = document.getElementById('peak_ld').getContext('2d');
var myChart1 = new Chart(peak_ld, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Peak Load',
            fill:false,
            data: [8, 8, 8, 8, 8, 8, 8 ,8, 8, 8, 8, 8, 8, 8,10],
            borderColor: 'rgba(0, 230, 64, 1)',
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



/*------------------------------------------JS for "Load in KVA" chart ------------------------------------------------*/
var ld_kva = document.getElementById('ld_kva').getContext('2d');
var myChart2 = new Chart(ld_kva, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Load in KVA',
            fill:false,
            data: [8, 8, 8, 8, 8, 8, 8 ,8, 8, 8, 8, 8, 8, 8,10],
            borderColor: 'rgba(0, 230, 64, 1)',
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
            text: 'Load in KVA',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Load in AMP" chart ------------------------------------------------*/

var ld_amp = document.getElementById('ld_amp').getContext('2d');
var myChart3 = new Chart(ld_amp, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Load in AMP',
            fill:false,
            data: [8, 8, 8, 11, 8, 8, 8 ,4, 8, 8, 1, 8, 8, 18,10],
            borderColor:'rgba(219, 10, 91, 1)',
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
            text: 'Load in AMP',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});