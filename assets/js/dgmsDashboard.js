
var ctx = document.getElementById('diesel_level').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['6:00', '9:00', '12:00', '3:00', '6:00', '9:00', '12:00','13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'],
        datasets: [{
            label: 'Diesel Level',
            // fill: false,
            data: [8, 8, 8, 8, 8, 6, 1,8, 8, 8, 8, 8, 8, 20],
            backgroundColor: "rgba(190, 144, 212,0.4)",
            borderColor: "rgba(190, 144, 212,0.5)",
            borderWidth: 2
        },
        {
            label: 'Diesel Level',
            fill: false,
            type: 'line',
            data: [8, 8, 8, 8, 8, 6, 1,8, 8, 8, 8, 8, 8, 20],
            borderColor:'rgba(155, 89, 182, 1)',
            borderWidth: 2
        },
        // {
        //     label: 'min diesel level',
        //     type: 'line',
        //     fill: false,
        //     data: [1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1],
        //     // backgroundColor: [
        //     //     'rgba(255, 255, 255, 0.4)'
                
        //     // ],
        //     borderColor: [
        //         'rgba(238, 238, 0, 1)'
               
        //     ],
        //     borderWidth: 2
        // },{
        //     label: 'max diesel level',
        //     type: 'line',
        //     fill: false,
        //     data: [12, 12, 12, 12, 12, 12, 12,12, 12, 12, 12, 12, 12, 12],
        //     // backgroundColor: [
        //     //     'rgba(255, 255, 255, 0.4)'
                
        //     // ],
        //     borderColor: [
        //         'rgba(240, 52, 52, 1)'
               
        //     ],
        //     borderWidth: 2
        // }
    ]
    },

    
    options: {
      
      legend: {
                
                labels: {
                    fontColor: "black",
                    fontSize: 13,
                    display: false
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
                    color: "rgba(0,0,0,0.3)",
                },
                ticks: {
                    fontColor: "black",
                    fontSize: 17
                }
            }]
        },

            title: {
                display: true,
                text: 'Diesel Level',
                fontSize: 17,
                fontColor: "balck",
                fontFamily: "Helvetica"
            }
    }
});
