import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({


    currentAlbumImage: {
        height: '400px',
        width: '400px'
    },

    albumDiv: {
        display: 'flex',
        flexBasis: 'row'
    },

    albumHeader: {
        textAlign: 'center'
    },

    currentAlbums: {
        display: 'flex',
        flexDirection: 'row'
   },

   albumList: {
       paddingLeft: '0px',
       overflow: 'hidden',
       overflowY: 'scroll',
       height: '710px',
   },

    albumListDiv: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
    },

    albumInfo: {
        display: 'flex',
        justifyContent: 'space-evenly',
        flexDirection: 'column',
        height: '100%'
    },

    membersDiv: {
        width: '310px'
    },

    albumListHead:{
        marginBottom: '5px',
        display: 'flex',
        width: '100%'
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
        marginBottom: '8px'
    },

    mandatoryHead: {
        marginLeft: '35px',
        textAlign: 'center'
    },

    optionalHead: {
        marginLeft: '70px',
        textAlign: 'center'
    },

    optional: {
        marginLeft: '8px',
        marginBottom: '8px',
        paddingLeft: '8px',
        borderLeft: '3px solid  rgba(0,0,0,.1)'
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
                    <a href={mand.url}>
                      <div>
                        <img src={mand.image} alt={mand.name} className={this.classes.currentAlbumImage}/>
                        <div>
                          <p className={this.classes.weeklyAlbumName}>{mand.name}</p>
                          <p className={this.classes.weeklyAlbumArtist}>{mand.artist}</p>
                        </div>
                      </div>
                    </a>
                  </div>
                  <div className={this.classes.optional}>
                    <p>Optional:</p>
                    <a href={opt.url}>
                      <div>
                        <img src={opt.image} alt={opt.name} className={this.classes.currentAlbumImage}  style={{height: '400px', width:'400px'}}/>
                        <div>
                          <p className={this.classes.weeklyAlbumName}>{opt.name}</p>
                          <p className={this.classes.weeklyAlbumArtist}>{opt.artist}</p>
                        </div>
                      </div>
                    </a>
                  </div>
                </div>
                <div>
                  <h2 style={{textAlign: 'center'}}>Our Rating Trend</h2>
                  <div className="chart-container">
                    <canvas id="ratingTrendChart"></canvas>
                  </div>
                </div>
              </div>)
    }
}

ThisWeeksAlbums.defaultProps = {
    previous: []
}

export default withStyles(styles)(ThisWeeksAlbums);
