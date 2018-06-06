'use strict';
/* global Chart moment */

document.addEventListener('DOMContentLoaded', function() {
  var labels = [],
    humidity = [],
    predictionLastDay = [];

  var ctx = document.getElementById('myChart');
  var measured = JSON.parse(
    document
      .querySelector('[data-measurements]')
      .getAttribute('data-measurements')
  );

  var predictions = JSON.parse(
    document
      .querySelector('[data-predictions]')
      .getAttribute('data-predictions')
  );

  for (var i = 0; i < measured.length; i++) {
    labels[i] = new Date(measured[i].measuredAt);
    humidity[i] = measured[i].humidity;
    predictionLastDay[i] = predictions[i].humidity;
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
        },
        {
          label: 'humidity(predicted)',
          backgroundColor: '#00ccff',
          data: predictionLastDay
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
