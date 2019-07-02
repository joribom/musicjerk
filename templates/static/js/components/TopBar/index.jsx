import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import Input from '@material-ui/core/Input';
import Button from '@material-ui/core/Button';
import Search from '@material-ui/icons/Search';
import withStyles from '@material-ui/core/styles/withStyles';
import authenticator from '../Authenticator';
import './styles.scss';

class TopBar extends Component {
  constructor (props) {
    super(props);
    this.classes = props.classes;
    authenticator.addStatusListener(this.forceUpdate, this);
  }

  render(){
    let user_handling;
    if (authenticator.validated()){
      user_handling = <NavLink className='link' to="/logout">Logout</NavLink>;
    } else {
      user_handling = <NavLink className='link' to="/login">Login</NavLink>;
    }
    return (
      <div className='topnav'>
        <NavLink className='link' exact={true} to="/">Home</NavLink>
        <NavLink className='link' to="/albums">Albums</NavLink>
        <NavLink className='link' to="/lyrics">Lyrics</NavLink>
        {user_handling}
        <div className='searchDiv'>
          <Input className='searchInput' type="text" placeholder="Search..."/>
          <Button className='searchButton' type="submit">
            <Search/>
          </Button>
        </div>
      </div>
    );
  }
}

export default TopBar;
