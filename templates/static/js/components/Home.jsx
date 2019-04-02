import React, { Component } from 'react';
import AlbumList from './AlbumList';
import ThisWeeksAlbums from './ThisWeeksAlbums';
import MemberList from './MemberList';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import withStyles from '@material-ui/core/styles/withStyles';
import { sizing } from '@material-ui/system';

const styles = theme => ({
    bodyDiv: {
        margin: '8px',
        marginTop: '0px',
        marginLeft: '0px',
        marginRight: '0px',
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        minHeight: '1080px'
    },

    thisWeekContainer: {
        display: 'flex',
        flexGrow: '1',
        justifyContent: 'center',
        backgroundColor: '#2c2f33',
        boxShadow: '0px 0px 15px #1b1a1a inset'
    },

    progress: {
        margin: theme.spacing.unit * 2,
    },

    membersDiv: {
        width: '310px'
    },
})

class Home extends Component {
    constructor(props){
        super(props);
        this.classes = props.classes;
        this.state = {
            thisWeek: null,
            loadingThisWeek: true,
            albums: [],
            loadingPrevious: true,
            members: [],
            loadingMembers: true
        }
    }

    componentDidMount(){
      fetch('/api/albums', {
        method: 'GET'
      }).then(response => response.json()
      .then(data => {
        console.log(data);
        this.setState((state, props) => {
          return {albums: data, loadingPrevious: false};
        });
      }));
    }

    render() {
      //const albums = [{name : 'test', url : '/test', image : 'https://i.scdn.co/image/06ed478c89f07a5e9daf7a59ec1c556a81952cd1'}];
      let albumList;
      if (this.state.loadingPrevious){
        albumList = <CircularProgress className={this.state.progress} />
      } else {
        albumList = <AlbumList albums={this.state.albums} />;
      }
      let thisWeek;
      if (this.state.loadingThisWeek){
        thisWeek = <CircularProgress className={this.state.progress} size='200' />
      } else {
        thisWeek = <ThisWeeksAlbums />;
      }
      let members;
      if (this.state.loadingMembers){
        members = <CircularProgress className={this.state.progress} />
      } else {
        members = <MemberList />;
      }
      return (
        <div className={this.classes.bodyDiv}>
          {albumList}
          <div className={this.classes.thisWeekContainer}>
            {thisWeek}
          </div>
          <div className={this.classes.membersDiv}>
          {members}
          </div>
        </div>
      );
    }
}

export default withStyles(styles)(Home);
