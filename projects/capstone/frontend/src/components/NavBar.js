import React from 'react';
import { useAuth0 } from '../react-auth0-spa';

const NavBar = () => {
    const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

    return (
        <>
          {!isAuthenticated && (
            <button onClick={() => window.location.replace(loginWithRedirect())}>Log in</button>
          )}
    
          {isAuthenticated && <button onClick={() => logout()}>Log out</button>}
        </>
      );
}

export default NavBar;