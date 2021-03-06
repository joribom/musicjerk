import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({

    thisWeek: {
        overflow: 'hidden',
        //overflowY: 'scroll',
    },

    currentAlbumImage: {
      width: '70%',
      height: 'auto',
      //height: '400px',
      //width: '400px',
    },

    albumHeader: {
        textAlign: 'center'
    },

    currentAlbums: {
        display: 'flex',
        flexDirection: 'row'
   },

    weeklyAlbumName: {
        textAlign: 'center',
        color: '#ffffff',
        fontSize: '20px',
        marginTop: '3px',
        marginBottom: '0px',
        textDecoration: 'none'
    },

    weeklyAlbumArtist: {
        textAlign: 'center',
        color: '#bbbbbb',
        marginTop: '0px',
        marginBottom: '3px',
        textDecoration: 'none'
    },

    mandatory: {
        marginLeft: '8px',
        marginBottom: '8px',
        width: '50%',
        textAlign: 'center',
    },

    optional: {
        marginLeft: '8px',
        marginBottom: '8px',
        paddingLeft: '8px',
        borderLeft: '3px solid  rgba(0,0,0,.1)',
        width: '50%',
        textAlign: 'center',
    }
});

class ThisWeeksAlbums extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
    }

    render () {
        const mand = this.props.albums[0];
        const opt = this.props.albums[1];
        return(
            <div className={this.classes.thisWeek}>
                <div className={this.classes.albumHeader}>
                  <h2>- This Week's Albums -</h2>
                </div>
                <div className={this.classes.currentAlbums}>
                  <div className={this.classes.mandatory}>
                    <p>Mandatory:</p>
                    <Link to={'/albums/' + mand.url}>
                      <div style={{textAlign: 'center'}}>
                        <img src={mand.image} alt={mand.name} className={this.classes.currentAlbumImage}/>
                        <div>
                          <p className={this.classes.weeklyAlbumName}>{mand.name}</p>
                          <p className={this.classes.weeklyAlbumArtist}>{mand.artist}</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className={this.classes.optional}>
                    <p>Optional:</p>
                    <Link to={'/albums/' + opt.url}>
                      <div style={{textAlign: 'center'}}>
                        <img src={opt.image} alt={opt.name} className={this.classes.currentAlbumImage}/>
                        <div>
                          <p className={this.classes.weeklyAlbumName}>{opt.name}</p>
                          <p className={this.classes.weeklyAlbumArtist}>{opt.artist}</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>)
    }
}

ThisWeeksAlbums.defaultProps = {
    previous: []
}

export default withStyles(styles)(ThisWeeksAlbums);
