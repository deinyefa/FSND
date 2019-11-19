import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Router, Route, Switch, Link } from "react-router-dom";

import NavBar from "./components/NavBar";
import { useAuth0 } from "./react-auth0-spa";
import { Movies } from './components/Movies';
import { Actors } from './components/Actors';
import history from "./utils/history";

function App() {
  const { loading } = useAuth0();

  if (loading) {
    return <img src={logo} className="App-logo" alt="logo" />;
  }

  return (
    <div className="App">
      <Router history={history}>
        <header className="App-header">
          <Link to='/'>
            <img src={logo} className="App-logo" alt="logo" />
          </Link>
          <NavBar />
        </header>

        <Switch>
          <Route path='/' exact />
          <Route path='/movies' component={Movies} />
          <Route path='/actors' component={Actors} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
