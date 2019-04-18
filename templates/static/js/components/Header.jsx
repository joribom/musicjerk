import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({
    text: {
        textTransform: 'capitalize'
    },
});


function Header(props) {
    const { classes } = props;
    const { cookies } = props;
    if (cookies.get('username') != ''){
      return (
        <div className="header">
          <h1 className={classes.text}>Big Musicjerk, logged in as {cookies.get('username')}</h1>
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
