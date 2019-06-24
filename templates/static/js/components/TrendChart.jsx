import React, { Component } from 'react';
import { Chart, Line } from 'react-chartjs-2';

class TrendChart extends Component {
    render() {
        const albumAverages = this.props.albumAverages;
        const type = 'scatter';
        const data = {
          datasets: [{
            label: "Rating Trend",
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: 'rgb(255, 99, 132)',
            data: albumAverages,
          }],
          labels: albumAverages.map(x => x.x),
        };
        const options = {
          onClick: function(_, chartElement) {
            if (chartElement.length > 0)
              window.location.href = `/albums/${albumAverages[chartElement[0]._index].url}`;
          },
          hover: {
            onHover: function(e, chartElement) {
              e.target.style.cursor = chartElement.length > 0 ? 'pointer' : 'default';
            }
          },
          tooltips: {
            custom: function(tooltip) {
              if (!tooltip) return;
              tooltip.displayColors = false;
            },
            callbacks: {
              title: function(tooltipItem, data) {
                return albumAverages[tooltipItem[0].index].title;
              },
              label: function(tooltipItem, data) {
                return `Average rating: ${tooltipItem.yLabel}`;
              }
            }
          },
          scales: {
            xAxes: [{
              ticks: {
                min: 1,
                stepSize: 20
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true,
                max: 10
              }
            }]
          }
        };
        return (
          <div>
            <h2 style={{textAlign: 'center'}}>Our Rating Trend</h2>
            <div className="chart-container">
              <canvas id="ratingTrendChart"></canvas>
            </div>
            <Line type={type} data={data} options={options}/>
          </div>
        );
    }
}

export default TrendChart;
