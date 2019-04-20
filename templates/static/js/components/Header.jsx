import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';
import authenticator from './Authenticator'

const styles = theme => ({
    text: {
        textTransform: 'capitalize'
    },
});


function Header(props) {
    const { classes } = props;
    const { cookies } = props;
    console.log('Checking validation...');
    console.log(authenticator.validated());
    if (authenticator.validated()){
      return (
        <div className="header">
          <h1 className={classes.text}>Big Musicjerk, logged in as {authenticator.}</h1>
        </div>
      )
  } else {
    return (
      <div className="header">
        <h1 className={classes.text}>Big Musicjerk</h1>
      </div>
    )
  }
}

export default withStyles(styles)(Header);
