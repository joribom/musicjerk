import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({
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
    },

    oldAlbumImage: {
        width: '130px',
        height: '130px'
    }
});

class AlbumList extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
    }

    render () {
        const albums = [];
        for (const index in this.props.albums){
            const [mand, opt] = this.props.albums[index];
            if (opt){
            albums.push(
                <div key={mand.name} className={this.classes.albumDiv}>
                  <div>
                    <a href={'/albums/' + mand.url}>
                      <div>
                        <img src={mand.image} alt={mand.name} className={this.classes.oldAlbumImage}/>
                      </div>
                    </a>
                  </div>
                  <div key={opt.name} className={this.classes.optional}>
                    <a href={'/albums/' + opt.url}>
                      <div>
                        <img src={opt.image} alt={opt.name} className={this.classes.oldAlbumImage}/>
                      </div>
                    </a>
                  </div>
                </div>);
            } else {
                albums.push(
                  <div key={mand.name} className={this.classes.mandatory}>
                    <a href={'/albums/' + mand.url}>
                      <div>
                        <img src={mand.image} alt={mand.name} className={this.classes.oldAlbumImage}/>
                      </div>
                    </a>
                  </div>);
            }
        }
        return (
          <div>
            <h2 style={{textAlign: 'center', marginTop: '20px', marginBottom: '20px'}}>Previous albums</h2>
            <div className={this.classes.albumListDiv}>
              <div className={this.classes.albumListHead}>
                <span className={this.classes.mandatoryHead}>Mandatory</span>
                <span></span>
                <span className={this.classes.optionalHead}>Optional</span>
              </div>
            </div>

            <ul id="albumList" className={this.classes.albumList}>
              <div className={this.classes.albumListDiv}>
                {albums}
              </div>
            </ul>
          </div>
        );
    }
}

export default withStyles(styles)(AlbumList);
