import React, { Component } from 'react';
import Link from '@material-ui/core/Link';
import CircularProgress from '@material-ui/core/CircularProgress';

class Albums extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
        this.state = {
            albums: [],
            loading: true,
        };
    }

    componentDidMount(){
        fetch('/api/album-averages', {
          method: 'GET'
        }).then(response => response.json()
        .then(data => {
          this.setState((state, props) => {
            console.log(data);
            return {albums: data, loading: false};
          });
        }));
    }

    render () {
        if (this.state.loading){
            return (<div style={{textAlign: 'center'}}><CircularProgress size='200'/></div>);
        }
        var albums = [];
        for (var index in this.state.albums) {
            var album = this.state.albums[index];
            albums.push(<li><Link key={album.title} href={'/albums/' + album.url }>{album.title}</Link></li>)
        }
        return (
          <div>
            <ol>
              {albums}
            </ol>
          </div>
        );
    }
}

export default Albums;
