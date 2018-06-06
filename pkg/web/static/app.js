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

function buildChartConfig(labels, datasets) {
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

  return {
    type: 'bubble',
    options: options,
    data: {
      labels: labels,
      datasets: datasets
    }
  };
}

document.addEventListener('DOMContentLoaded', function() {
  Chart.defaults.global.defaultFontColor = '#FFF';

  // chart for the 24h forecast
  var forecastChart = document.getElementById('forecastChart');
  var forecastData = extractData('data-next-day');
  var forecastHumidity = buildData(forecastData, 'humidity');
  var forecastLabels = buildLabels(forecastData);
  var forecastConfig = buildChartConfig(forecastLabels, [
    {
      label: 'humidity(predicted)',
      backgroundColor: '#DC572E',
      data: forecastHumidity
    }
  ]);

  new Chart(forecastChart, forecastConfig);

  // chart for the previous 24h
  var previousDayChart = document.getElementById('previousDayChart');

  var previousDayMeasured = extractData('data-measurements');
  var previousDayPredicted = extractData('data-predictions');
  var previousDayHumidity = buildData(previousDayMeasured, 'humidity');
  var previousDayForeCast = buildData(previousDayPredicted, 'humidity');
  var previousDayLabels = buildLabels(previousDayMeasured);

  var last24hConfig = buildChartConfig(previousDayLabels, [
    {
      label: 'humidity(measured)',
      backgroundColor: '#2672EC',
      data: previousDayHumidity
    },
    {
      label: 'humidity(predicted)',
      backgroundColor: '#DC572E',
      data: previousDayForeCast
    }
  ]);

  new Chart(previousDayChart, last24hConfig);
});
