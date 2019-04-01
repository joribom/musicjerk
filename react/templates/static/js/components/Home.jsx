import React, { Component } from 'react';
import AlbumList from './AlbumList';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';

export default class Home extends Component {
    constructor(props){
        super(props);
        this.state = {
            albums: [],
            loading: true
        }
    }

    componentDidMount(){
      fetch('/api/albums', {
        method: 'GET'
      }).then(response => response.json()
      .then(data => {
        console.log(data);
        this.setState((state, props) => {
          return {albums: data, loading: false};
        });
      }));
    }

    render() {
      //const albums = [{name : 'test', url : '/test', image : 'https://i.scdn.co/image/06ed478c89f07a5e9daf7a59ec1c556a81952cd1'}];
      let albumlist;
      if (this.state.loading){
        albumlist = <CircularProgress />;
      } else {
        albumlist = <AlbumList albums={this.state.albums} />;
      }
      return (
        <div>
          {albumlist}
        </div>
      );
    }
}
