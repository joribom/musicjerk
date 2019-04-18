import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import Input from '@material-ui/core/Input';
import Button from '@material-ui/core/Button';
import Search from '@material-ui/icons/Search';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({
    searchDiv: {
        padding: '8px',
        display: 'flex',
        flexDirection: 'row',
        float: 'right',
        alignItems: 'center'
    },

    searchInput: {
        border: 'none',
        backgroundColor: '#ffffff',
        fontSize: '18px',
        height: '30px',
        padding: '6px'
    },

     searchButton: {
        padding: '6px 10px',
        marginRight: '16px',
        background: '#ddd',
        fontSize: '17px',
        border: 'none',
        cursor: 'pointer',
        height: '42px',
        width: '44px',
        fontFamily: 'Montserrat, sans-serif',
        color: '#ffffff'
    }
});

function TopBar(props) {
    const { classes } = props;
    const { cookies } = props;
    let user_handling;
    if (cookies.get('uid') == ''){
        user_handling = <NavLink to="/login">Login</NavLink>;
    } else {
        user_handling = <NavLink to="/logout">Logout</NavLink>;
    }
    return (
      <div className="topnav">
        <NavLink exact={true} to="/">Home</NavLink>
        <NavLink to="/albums">Albums</NavLink>
        <NavLink to="/lyrics">Lyrics</NavLink>
        {user_handling}
        <div className={classes.searchDiv}>
          <Input className={classes.searchInput} type="text" placeholder="Search..."/>
          <Button className={classes.searchButton} type="submit">
            <Search/>
          </Button>
        </div>
      </div>
    );
}

export default withStyles(styles)(TopBar);
