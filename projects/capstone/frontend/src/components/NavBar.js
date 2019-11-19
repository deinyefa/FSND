import React from 'react';
import { useAuth0 } from '../react-auth0-spa';
import { Button } from 'reactstrap';
import { Link } from 'react-router-dom'

const NavBar = () => {
    const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

    return (
        <>
          <Link to='/movies'>Movies</Link>
          <Link to='/actors'>Actors</Link>
          {!isAuthenticated && (
            <Button onClick={() => window.location.replace(loginWithRedirect())}>Log in</Button>
          )}
    
          {isAuthenticated && <Button onClick={() => logout()}>Log out</Button>}
        </>
      );
}

export default NavBar;