import React from 'react';
import { BrowserRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import TopBar from './components/TopBar';
import AlbumPage from './components/AlbumPage';
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
        <Route path="/albums/:id" component={AlbumPage} />
     </div>
    </Router>
  );
}

export default AppRouter;
