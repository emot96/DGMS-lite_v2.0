/*------------------------------------------JS for "Input Voltage" chart ------------------------------------------------*/

var inV = document.getElementById('inV').getContext('2d');
var myChart1 = new Chart(inV, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Input Voltage',
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
            text: 'Input Voltage (VLL)',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});



/*------------------------------------------JS for "Output Voltage" chart ------------------------------------------------*/
var outV = document.getElementById('outV').getContext('2d');
var myChart2 = new Chart(outV, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Output Voltage',
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
            text: 'Output Voltage (VLL)',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "O/P VLN Average" chart ------------------------------------------------*/

var vln_avg = document.getElementById('vln_avg').getContext('2d');
var myChart3 = new Chart(vln_avg, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'],
        datasets: [{
            label: 'Output Voltage VLN Average',
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
            text: 'Output Voltage VLN Average',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
    }
});


/*------------------------------------------JS for "Power Factor" chart ------------------------------------------------*/

var pow_fac = document.getElementById('pow_fac').getContext('2d');
var myChart3 = new Chart(pow_fac, {
    type: 'line',
    data: {
        labels: ['08:00', '08:01', '08:02', '08:03', '08:04', '08:05', '08:06', '08:07', '08:08', '08:09', '08:10', '08:11', '08:12', '08:13', '08:14', '08:15', '08:16', '08:17', '08:18', '08:19', '08:20', '08:21', '08:22', '08:23', '08:24', '08:25', '08:26', '08:27', '08:28', '08:29', '08:30', '08:31', '08:32', '08:33', '08:34', '08:35', '08:36', '08:37', '08:38', '08:39', '08:40', '08:41', '08:42', '08:43', '08:44', '08:45', '08:46', '08:47', '08:48', '08:49', '08:50', '08:51', '08:52', '08:53', '08:54', '08:55', '08:56', '08:57', '08:58', '08:59', '09:00', '09:01', '09:02', '09:03', '09:04', '09:05', '09:06', '09:07', '09:08', '09:09', '09:10', '09:11', '09:12', '09:13', '09:14', '09:15', '09:16', '09:17', '09:18', '09:19', '09:20', '09:21', '09:22', '09:23', '09:24', '09:25', '09:26', '09:27', '09:28', '09:29', '09:30', '09:31', '09:32', '09:33', '09:34', '09:35', '09:36', '09:37', '09:38', '09:39', '09:40', '09:41', '09:42', '09:43', '09:44', '09:45', '09:46', '09:47', '09:48', '09:49', '09:50', '09:51', '09:52', '09:53', '09:54', '09:55', '09:56', '09:57', '09:58', '09:59', '10:00', '10:01', '10:02', '10:03', '10:04', '10:05', '10:06', '10:07', '10:08', '10:09', '10:10', '10:11', '10:12', '10:13', '10:14', '10:15', '10:16', '10:17', '10:18', '10:19', '10:20', '10:21', '10:22', '10:23', '10:24', '10:25', '10:26', '10:27', '10:28', '10:29', '10:30', '10:31', '10:32', '10:33', '10:34', '10:35', '10:36', '10:37', '10:38', '10:39', '10:40', '10:41', '10:42', '10:43', '10:45', '10:46', '10:47', '10:48', '10:49', '10:50', '10:51', '10:52', '10:53', '10:54', '10:55', '10:56', '10:57', '10:58', '10:59', '11:00', '11:01', '11:02', '11:03', '11:04', '11:06', '11:07', '11:08', '11:09', '11:10', '11:11', '11:12', '11:13', '11:14', '11:15', '11:16', '11:17', '11:18', '11:19', '11:20', '11:21', '11:22', '11:24', '11:25', '11:26', '11:27', '11:31', '11:32', '11:34', '11:35', '11:36', '11:37', '11:38', '11:39', '11:40', '11:42', '11:43', '11:44', '11:45', '11:46', '11:47', '11:48', '11:49', '11:50', '11:51', '11:52', '11:57', '11:58', '11:59', '12:00', '12:01', '12:02', '12:03', '12:04', '12:05', '12:06', '12:07', '12:08', '12:09', '12:10', '12:11', '12:12', '12:13', '12:14', '12:15', '12:16', '12:17', '12:18', '12:19', '12:21', '12:22', '12:23', '12:24', '12:25', '12:26', '12:27', '12:28', '12:29', '12:30', '12:31', '12:33', '12:34', '12:35', '12:36', '12:37', '12:38', '12:39', '12:40', '12:41', '12:42', '12:43', '12:44', '12:45', '12:46', '12:47', '12:48', '12:49', '12:50', '12:51', '12:52', '12:53', '12:54', '12:55', '12:56', '12:57', '12:58', '12:59', '13:00', '13:01', '13:02', '13:03', '13:05', '13:06', '13:07', '13:08', '13:09', '13:10', '13:11', '13:12', '13:13', '13:14', '13:15', '13:16', '13:17', '13:18', '13:19', '13:20', '13:21', '13:22', '13:23', '13:25', '13:26', '13:27', '13:28', '13:29', '13:30', '13:31', '13:32', '13:33', '13:34', '13:35', '13:36', '13:37', '13:38', '13:39', '13:41', '13:42', '13:44', '13:45', '13:46', '13:47', '13:48', '13:49', '13:52', '13:53', '13:54', '13:55', '13:56', '13:57', '13:58', '13:59', '14:02', '14:04', '14:05', '14:07', '14:08', '14:09', '14:10', '14:11', '14:12', '14:13', '14:14', '14:15', '14:16', '14:17', '14:18', '14:20', '14:21', '14:22', '14:23', '14:24', '14:25', '14:26', '14:28'],
        datasets: [{
            label: 'Power Factor',
            fill:false,
            data: [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 28, 28, 28, 28, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27],
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
                // type: 'linear',
                gridLines: {
                    color: "rgba(0,0,0,0.3)",
                },
                ticks: {
                    fontColor: "black",
                    beginAtZero: true,
                    fontSize: 10,
                }
            }],

            xAxes: [{
                // type: 'time',
                gridLines: {
                    color: "rgba(0,0,0,0)",
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 10,
                    autoSkip: true,
                    maxTicksLimit: 60,
                    maxRotation: 0
                    
                    
                }
            }]
        },
        plugins: {
            title: {
              display: true,
              text: 'Power Factor',
              fontSize: 17,
              fontColor: "balck",
              fontFamily: "Helvetica"
            },
            zoom: {
              pan: {
                enabled: true,
                mode: 'x',
                // overScaleMode: 'y'
              },
              zoom: {
                enabled: true,
                mode: 'x',
                // drag: true,
                speed: 0.00001,
                threshold: 0,
                sensitivity: 0
                // overScaleMode: 'y'
              }
            }
          },
          
    },
        
    });