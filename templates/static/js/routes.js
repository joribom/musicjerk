import React from 'react';
import { BrowserRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import TopBar from './components/TopBar';
// import more components

function Topics({ match }) {
  return (
    <div>
      <h2>Topics</h2>
      <ul>
        <li>
          <Link to={`${match.url}/rendering`}>Rendering with React</Link>
        </li>
        <li>
          <Link to={`${match.url}/components`}>Components</Link>
        </li>
        <li>
          <Link to={`${match.url}/props-v-state`}>Props v. State</Link>
        </li>
      </ul>

      <Route path={`${match.path}/:topicId`} component={Topic} />
      <Route
        exact
        path={match.path}
        render={() => <h3>Please select a topic.</h3>}
      />
    </div>
  );
}

function Topic({ match }) {
  return (
    <div>
      <h3>{match.params.topicId}</h3>
    </div>
  );
}

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
        <Route path="/topics" component={Topics} />
     </div>
    </Router>
  );
}

export default AppRouter;
