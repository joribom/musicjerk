import React from 'react';
import { Redirect } from 'react-router-dom';
import authenticator from './Authenticator';

function Logout(props){
    var { cookies } = props;
    console.log('In here!');
    authenticator.signOut()
    return <Redirect to='/' />
}

export default Logout;
