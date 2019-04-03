import React from 'react';
import { BrowserRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Albums from './components/Albums';
import TopBar from './components/TopBar';
import AlbumPage from './components/AlbumPage';
import MemberPage from './components/MemberPage';
// import more components

function AppRouter() {
  return (
//export default (
    <Router>
     <div>
         <div className="header">
           <h1 className="head-text">BIG Musicjerk</h1>
         </div>
        <TopBar />

        <Route exact path="/" component={Home} />
        <Route path="/login" component={Login} />
        <Route exact path="/albums" component={Albums} />
        <Route path="/albums/:id" component={AlbumPage} />
        <Route path="/member/:id" component={MemberPage} />
     </div>
    </Router>
  );
}

export default AppRouter;
