import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import Link from '@material-ui/core/Link';
import { Bar, Line } from 'react-chartjs-2';

class MemberPage extends Component {
    constructor(props){
        super(props);
        this.classes = props.classes;
        this.state = {
            data: null,
            loading: true,
        }
    }

    componentDidMount(){
      const id = this.props.match.params.id;
      fetch('/api/member/' + id, {
        method: 'GET'
      }).then(response => response.json()
      .then(data => {
        this.setState((state, props) => {
          console.log(data);
          return {data: data, loading: false};
        });
      }));
    }
    render() {
        if (this.state.loading){
            return (<CircularProgress size='200' />)
        }
        const scores = this.state.data.albums;
        const data = {
          datasets: [{
            label: "Rating Trend",
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: 'rgb(255, 99, 132)',
            data: scores,
          }],
          labels: scores.map(x => x.x),
        };
        const options = {
          onClick: function(_, chartElement) {
            if (chartElement.length > 0)
              window.location.href = `/albums/${scores[chartElement[0]._index].url}`;
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
                return scores[tooltipItem[0].index].title;
              },
              label: function(tooltipItem, data) {
                return `Rating: ${tooltipItem.yLabel}`;
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
        var likeness = [];
        for (var index in this.state.data.likeness){
            var entry = this.state.data.likeness[index];
            likeness.push(<li key={entry[0]}><Link href={'/member/' + entry[0].toLowerCase()}>{entry[0]}</Link>: {entry[1]}%</li>)
        }
        return (
            <div style={{width: '50%'}}>
              <Line data={data} options={options}/>
              <ol>
                {likeness}
              </ol>
            </div>);
    }
}

export default MemberPage;
