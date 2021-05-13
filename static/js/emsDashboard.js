/*------------------------------------------JS for "Current RBY" chart ------------------------------------------------*/

var cur_rby = document.getElementById('cur_rby').getContext('2d');
var chart1 = new Chart(cur_rby, {
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
                      color: "rgba(0,0,0,0.1)",
                  },
                  ticks: {
                      fontColor: "black",
                      beginAtZero: true,
                      fontSize: 17
                  }
              }],
  
              xAxes: [{
                  gridLines: {
                      color: "rgba(0,0,0,0.1)",
                  },
                  ticks: {
                      fontColor: "black",
                      fontSize: 17
                  }
              }]
          },

          title: {
            display: true,
            text: 'Phasewise Current',
            fontSize: 17,
            fontColor: "balck",
            fontFamily: "Helvetica"
        }
      }
});
         
