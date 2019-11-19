import React from 'react';
import logo from './logo.svg';
import './App.css';

import NavBar from "./components/NavBar";
import { useAuth0 } from "./react-auth0-spa";

function App() {
  const { loading } = useAuth0();

  if (loading) {
    return <img src={logo} className="App-logo" alt="logo" />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <NavBar />
      </header>
    </div>
  );
}

export default App;
