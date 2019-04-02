import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({

});

class ThisWeeksAlbums extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
    }

    render () {
        return(<div></div>)
    }
}

export default withStyles(styles)(ThisWeeksAlbums);
