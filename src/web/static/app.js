'use strict';
/* global Chart */

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
          label: 'humidity',
          backgroundColor: '#FF69B4',
          data: humidity
        }
      ]
    },
    options: {
      scales: {
        xAxes: [
          { type: 'time', time: { unit: 'hour' }, gridLines: { color: '#555' } }
        ]
      }
    }
  });
});
