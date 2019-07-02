import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';
import authenticator from '../Authenticator'
import './styles.scss';

class Header extends Component {

  constructor(props){
    super(props);
    this.classes = props.classes;
    authenticator.addStatusListener(this.forceUpdate, this);
  }

  render() {
    return (
      <div className='header'>
          <h1>Big Musicjerk{
              authenticator.validated()
              ? (', logged in as ' + authenticator.username())
              : ''
          }</h1>
      </div>
      )
  }
}

export default Header;
