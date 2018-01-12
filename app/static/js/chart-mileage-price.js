const testData = [
  {'x':20000,'y':25000},
  {'x':40000,'y':20000},
  {'x':60000,'y':17500},
  {'x':80000,'y':15000},
  {'x':100000,'y':12500},
  {'x':120000,'y':10000}
]

var ctx = document.getElementById("chart-mileage-price").getContext("2d");
var myChart = new Chart.Scatter(ctx, {
  data: {
    datasets: [{
      label: "Honda S2000",
      data: testData,
      backgroundColor: 'rgba(54,162,235,0.1)',
      borderColor: 'rgba(54,162,235,1)',
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero:true
        },
        scaleLabel: {
          display: true,
          labelString: "price (USD)"
        }
      }],
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: "mileage (miles)"
        }
      }]
    }
  }
});
