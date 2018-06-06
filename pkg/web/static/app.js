'use strict';
/* global Chart moment */

function buildLabels(dataset) {
  var labels = [];
  for (var i = 0; i < dataset.length; i++) {
    labels[i] = new Date(dataset[i].measuredAt);
  }
  return labels;
}

function buildData(dataset, attribute) {
  var data = [];
  for (var i = 0; i < dataset.length; i++) {
    data[i] = dataset[i][attribute];
  }
  return data;
}

function extractData(attributeName) {
  return JSON.parse(
    document
      .querySelector('[' + attributeName + ']')
      .getAttribute(attributeName)
  );
}

document.addEventListener('DOMContentLoaded', function() {
  var options = {
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
        {
          type: 'time',
          time: { unit: 'hour' },
          gridLines: { color: '#555' }
        }
      ]
    }
  };

  var labels = [],
    humidity = [],
    predictions = [],
    i;

  var ctx = document.getElementById('myChart');
  var measured = JSON.parse(
    document
      .querySelector('[data-measurements]')
      .getAttribute('data-measurements')
  );

  var predicted = JSON.parse(
    document
      .querySelector('[data-predictions]')
      .getAttribute('data-predictions')
  );

  for (i = 0; i < measured.length; i++) {
    humidity[i] = measured[i].humidity;
  }

  for (i = 0; i < predicted.length; i++) {
    labels[i] = new Date(predicted[i].measuredAt);
    predictions[i] = predicted[i].humidity;
  }
  Chart.defaults.global.defaultFontColor = '#FFF';

  new Chart(ctx, {
    type: 'bubble',
    data: {
      labels,
      datasets: [
        {
          label: 'humidity(measured)',
          backgroundColor: '#2672EC',
          data: humidity
        },
        {
          label: 'humidity(predicted)',
          backgroundColor: '#DC572E',
          data: predictions
        }
      ]
    },
    options: options
  });
});
