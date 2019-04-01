import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({
    albumDiv: {
        display: 'flex',
        flexBasis: 'row'
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
            const album = this.props.albums[index];
            albums.push(
                <div className={this.classes.albumDiv}>
                  <div>
                    <a href={album.url}>
                      <div>
                        <img src={album.image} alt={album.name} className="old-album-image"/>
                      </div>
                    </a>
                  </div>
                </div>
            );
        }
        return (
          <div className="album-div">
            <h2>Previous albums</h2>
            <div className="album-list-div">
              <div className="album-list-head">
                <span className="mandatory-head">Mandatory</span>
                <span></span>
                <span className="optional-head">Optional</span>
              </div>
            </div>

            <ul id="album-list">
                <div className="album-div">
                    {albums}
                </div>
            </ul>
          </div>
        );
    }
}

export default withStyles(styles)(AlbumList);
