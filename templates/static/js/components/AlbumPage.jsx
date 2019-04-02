import React, { Component } from 'react';
import AlbumList from './AlbumList';
import ThisWeeksAlbums from './ThisWeeksAlbums';
import MemberList from './MemberList';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import withStyles from '@material-ui/core/styles/withStyles';
import { sizing } from '@material-ui/system';

const styles = theme => ({

    membersDiv: {
        width: '310px'
    },
})

class AlbumPage extends Component {
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
      fetch('/api/albums/' + id, {
        method: 'GET'
      }).then(response => response.json()
      .then(data => {
        console.log(data);
        this.setState((state, props) => {
          return {data: data, loading: false};
        });
      }));
    }

    render_styles(){
        var styles = [];
        for (const index in this.state.data.styles){
            const style = this.state.data.styles[index];
            styles.push(<li key={style}>{ style }</li>);
        }
        return styles;
    }

    render_genres(){
        var genres = [];
        for (const index in this.state.data.genres){
            const genre = this.state.data.genres[index];
            genres.push(<li key={genre}>{ genre }</li>);
        }
        return genres;
    }

    render() {
        console.log("Big test!");
        if (this.state.loading){
            return (<CircularProgress size='200' />)
        }
        const genres = this.render_genres();
        const styles = this.render_styles();
        return (
            <div>
              <div style={{width:'100%'}}>
                <h1>{this.state.data.name}</h1>
                <h2>by { this.state.data.artist }</h2>
                <p>{ this.state.data.summary }</p>
              </div>
              <div style={{width:'100%', float:'left'}}>
                <img src={ this.state.data.image } style={{maxWidth:'50%', maxHeight:'50%', verticalAlign:'top'}} alt={ this.state.data.name }></img>
                <iframe src={"https://open.spotify.com/embed/album/" + this.state.data.spotify_id} style={{verticalAlign: 'bottom'}} width="500" height="500" allowtransparency="true" allow="encrypted-media"></iframe>
              </div>
              <div style={{ width:'45%', float:'left' }}>
                <h1>Genres:</h1>
                <ol id="genre_list">
                  {genres}
                </ol>
              </div>
              <div style={{width:'45%', float:'right'}}>
                <h1>Styles:</h1>
                <ol id="album_list">
                  {styles}
                </ol>
              </div>
            </div>
        );
    }
}

export default withStyles(styles)(AlbumPage);
