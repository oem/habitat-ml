'use strict';
/* global Chart moment */

document.addEventListener('DOMContentLoaded', function() {
  var labels = [],
    humidity = [];

  var ctx = document.getElementById('myChart');
  var data = JSON.parse(
    document
      .querySelector('[data-measurements]')
      .getAttribute('data-measurements')
  );

  for (var i = 0; i < data.length; i++) {
    labels[i] = new Date(data[i].measuredAt);
    humidity[i] = data[i].humidity;
  }
  Chart.defaults.global.defaultFontColor = '#FFF';

  new Chart(ctx, {
    type: 'bubble',
    data: {
      labels,
      datasets: [
        {
          label: 'humidity(measured)',
          backgroundColor: '#FF69B4',
          data: humidity
        }
      ]
    },
    options: {
      tooltips: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(tooltipItem, data) {
            var label = data.datasets[tooltipItem.datasetIndex].label || '';
            var formattedDate = moment(labels[tooltipItem.index]).format(
              'h:mm a'
            );

            label += ' ' + formattedDate + ': ';
            label += tooltipItem.yLabel + '%';
            return label;
          }
        }
      },
      scales: {
        xAxes: [
          { type: 'time', time: { unit: 'hour' }, gridLines: { color: '#555' } }
        ]
      }
    }
  });
});
