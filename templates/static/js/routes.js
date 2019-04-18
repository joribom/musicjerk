import React from 'react';
import { CookiesProvider, withCookies } from 'react-cookie';
import { BrowserRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import Header from './components/Header'
import Home from './components/Home';
import Login from './components/Login';
import Logout from './components/Logout';
import Albums from './components/Albums';
import TopBar from './components/TopBar';
import AlbumPage from './components/AlbumPage';
import MemberPage from './components/MemberPage';
// import more components

function AppRouter(props) {
  return (
//export default (
    <CookiesProvider>
      <Router>
        <div>
          <Header cookies={props.cookies} />
          <TopBar cookies={props.cookies} />

          <Route exact path="/" component={Home} />
          <Route path="/login" render={() => <Login cookies={props.cookies} />}/>
          <Route path="/logout" render={() => <Logout cookies={props.cookies} />}/>
          <Route exact path="/albums" component={Albums} />
          <Route path="/albums/:id" component={AlbumPage} />
          <Route path="/member/:id" component={MemberPage} />
        </div>
      </Router>
    </CookiesProvider>
  );
}

export default withCookies(AppRouter);
