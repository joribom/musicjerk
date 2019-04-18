import React from 'react'
import { Redirect } from 'react-router-dom'

function Logout(props){
    var { cookies } = props;

    cookies.set('uid', '', { path: '/' });
    cookies.set('session', '', { path: '/' });
    cookies.set('username', '', { path: '/' });

    return <Redirect to='/' />
}

export default Logout;
