/*------------------------------------------JS for "Diesel Level" chart ------------------------------------------------*/

var diesel_lev = document.getElementById('diesel_level1').getContext('2d');
var chart1 = new Chart(diesel_lev, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00','15:00', '16:00','17:00', '18:00'],
        datasets: [{
            label: 'Diesel Level',
            data: [8, 8, 8, 5, 5, 3, 11, 5,6,6,6,6,6,7],
            backgroundColor: [
                'rgba(0, 230, 64, 0.2)'
                
            ],
            borderColor: [
                'rgba(0, 230, 64, 1)'
               
            ],
            borderWidth: 1
        }]
    },
    options: {
      legend: {
               display:false
            },

        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "black",
                    fontSize: 15,
                    beginAtZero: true
                }
            }],

            xAxes: [{
                ticks: {
                    fontSize: 15,
                    fontColor: "black",
                }
            }]
        }
    }
});



/*------------------------------------------JS for "GSM Signal" chart ------------------------------------------------*/

var gsm = document.getElementById('gsm').getContext('2d');
var chart13 = new Chart(gsm, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00'],
        datasets: [{
            label: 'GSM Signal',
            data: [11,11,1,1,1,0,1],

            backgroundColor: [
                'rgba(0, 230, 64, 0.2)'
                
            ],
            borderColor: [
                'rgba(0, 230, 64, 1)'
               
            ],
            borderWidth: 1
        }]
    },
    options: {
      legend: {
           
        display:false
      
      },

        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "black",
                    fontSize: 15,
                    beginAtZero: true
                }
            }],

            xAxes: [{
                ticks: {
                    fontSize: 15,
                    fontColor: "black",
                }
            }]
        }
    }
});

/*------------------------------------------JS for "Gateway Battery" chart ------------------------------------------------*/

var gt_battery = document.getElementById('gt_battery').getContext('2d');
var chart14 = new Chart(gt_battery, {
    type: 'line',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00'],
        datasets: [{
            label: 'gateway battery',
            data: [11,11,1,1,1,0,1],

            backgroundColor: [
                'rgba(241, 130, 141,0.2)'
                
            ],
            borderColor: [
                'rgba(241, 130, 141,1)'
               
            ],
            borderWidth: 1
        }]
    },
    options: {
      legend: {
           
        display:false
      
      },

        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "black",
                    fontSize: 15,
                    beginAtZero: true
                }
            }],

            xAxes: [{
                ticks: {
                    fontSize: 15,
                    fontColor: "black",
                }
            }]
        }
    }
});