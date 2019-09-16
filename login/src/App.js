import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn } from 'mdbreact';
import NavbarPage from './Navbarpage';
import Login from './login';
import Nu_login from './Nu_login'
import Home from './home';
import Nu_desksignin from './nu_desksignin';
import NU_desklogin from './nu_desklogin';
function App() {
  return (
    <div className="App">
        {/* <NavbarPage/> */}
        <NavbarPage/>
    </div>
  );
}

export default App;
