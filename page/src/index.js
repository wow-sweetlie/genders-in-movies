import Chart from 'chart.js';
import data from './data.json';
import fontawesome from '@fortawesome/fontawesome'
import { faGithub, faTwitter } from '@fortawesome/fontawesome-free-brands'
require('./style.scss');

const red = 'rgb(255, 99, 132)';
const yellow = 'rgb(255, 205, 86)';


fontawesome.library.add(faGithub)
fontawesome.library.add(faTwitter)

function womenLine(data) {
  return data.data.map(year => (year.women/(year.women+year.men) * 100))
}

function parityLine(data) {
  return data.data.map(() => 50)
}

function years(data) {
  return data.data.map(year => year.year)
}

window.onload = function() {
  const chartElem = document.getElementById('graph');
  const ctx = chartElem.getContext('2d');
  window.chart = new Chart(ctx,{
    type: 'line',
    data: {
      datasets: [
        {
          label: "women",
          data: womenLine(data),
          backgroundColor: red,
        }
      ],
      labels: years(data),
    },
    options: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Women presence in first roles",
      },
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            var label = data.datasets[tooltipItem.datasetIndex].label || '';

            if (label) {
              label += ': ';
            }
            label += Math.round(tooltipItem.yLabel * 100) / 100;
            label += ' %';
            return label;
          }
        }
      },
      scales: {
        yAxes: [{
          type: 'linear',
          display: true,
          ticks: {
            min: 0,
            max: 100,
            callback: function(value, index, values) {
              return value + '%';
            }
          }
        }],
        xAxes: [{
          display: true,
            scaleLabel: {
              display: true,
              labelString: 'year'
          },
          ticks: {
            min: 1930,
            max: 2017,
            stepSize: 1,
          }
        }]

      },
      responsive: true,
    }
  });
};

