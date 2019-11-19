import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Router, Route, Switch } from "react-router-dom";

import NavBar from "./components/NavBar";
import { useAuth0 } from "./react-auth0-spa";
import { Movies } from './components/Movies';
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
          <img src={logo} className="App-logo" alt="logo" />
          <NavBar />
        </header>

        <Switch>
          <Route path='/' exact />
          <Route path='/movies' component={Movies} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
