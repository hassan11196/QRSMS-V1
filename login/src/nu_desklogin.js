import React, { Component } from "react";
import {MDBNavbar, MDBNavbarNav, MDBNavItem, MDBNavLink,} from "mdbreact";
import { BrowserRouter as Router } from 'react-router-dom';
import Nu_login from './Nu_login';
class NU_desklogin extends Component
{
    render(){
        return(

            <Router>
      <MDBNavbar color="indigo" dark expand="md">
        <MDBNavbarNav right>
          <MDBNavItem>
              <MDBNavLink to="#!">Haven't Register? Sign Up</MDBNavLink>
          </MDBNavItem>
          </MDBNavbarNav>
        </MDBNavbar>
      <Nu_login/>
    </Router>
        );
    }
}
export default NU_desklogin;