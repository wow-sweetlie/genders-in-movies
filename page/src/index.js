import Chart from 'chart.js';

const red = 'rgb(255, 99, 132)';
const yellow = 'rgb(255, 205, 86)';

window.onload = function() {
  const chartElem = document.createElement('canvas');
  document.body.appendChild(chartElem);
  const ctx = chartElem.getContext('2d');
  window.myPie = new Chart(ctx,{
    type: 'pie',
    data: {
      datasets: [{
        data: [
          30,
          70,
        ],
        backgroundColor: [
          red,
          yellow,
        ]
      }],
      labels: [
        'women',
        'men',
      ],
    },
    options: {
      responsive: true,
    }
  });
};

