import React, { Component } from "react";
import { MDBNavbar, MDBNavbarNav, MDBNavItem, MDBNavLink, MDBNavbarToggler, MDBCollapse, MDBDropdown, MDBDropdownToggle, MDBDropdownMenu, MDBDropdownItem } from "mdbreact";

// import Course_Registration from './course_registration';
import Home from './Home';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

class NavbarPage extends Component {
  state = {
    isOpen: false
  };

  toggleCollapse = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  render() {
    return (
      <Navbar collapseOnSelect expand="lg" fixed="top" bg="primary" variant="dark">
        <Navbar.Brand NavLink to="/home">Welcome To Student Portal</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <MDBNavLink to="/home">Home</MDBNavLink>
            <MDBNavLink to="/attendance">Attendance</MDBNavLink>
            <MDBNavLink to="/marks">Marks</MDBNavLink>
            <MDBNavLink to="/transcript">Transcript</MDBNavLink>
            <MDBNavLink to="/feechallan">Fee Challan</MDBNavLink>
            <MDBNavLink to="/feedetails">Fee Details</MDBNavLink>
             {/* <NavDropdown title="Dropdown" id="collasible-nav-dropdown">

              <NavDropdown.Item NavLink to="/transcript">Action</NavDropdown.Item>
              <NavDropdown.Item NavLink to="/attendance">Another action</NavDropdown.Item>
              <NavDropdown.Item NavLink to="/marks">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
            </NavDropdown> */}
          </Nav> 
          <Nav>
            <Nav.Link href="#deets">Logout</Nav.Link>
            {/* //<Nav.Link eventKey={2} href="#memes">
              Dank memes
      </Nav.Link> */}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      //  <MDBNavbar fixed="top"color="indigo" dark expand="md">

      //   <MDBNavbarToggler onClick={this.toggleCollapse} />
      //   <MDBCollapse id="navbarCollapse3" isOpen={this.state.isOpen} navbar>
      //     <MDBNavbarNav left>
      //       <MDBNavItem>
      //         <MDBNavLink to="/home">Home</MDBNavLink>
      //       </MDBNavItem>
      //       <MDBNavItem>
      //         <MDBNavLink to="./course_registration">Course Registration</MDBNavLink>
      //       </MDBNavItem>
      //       <MDBNavItem>
      //         <MDBNavLink to="/attendance">Attendance</MDBNavLink>
      //       </MDBNavItem>
      //       <MDBNavItem>
      //         <MDBDropdown>
      //           <MDBDropdownToggle nav caret>
      //             <span className="mr-2">Fee</span>
      //           </MDBDropdownToggle>
      //           <MDBDropdownMenu>
      //           <MDBDropdownItem to="'/feechallan'">Fee Challan</MDBDropdownItem>
      //           <mdb-dropdown-item to="/feechallan">Action</mdb-dropdown-item>
      //             <MDBNavLink to="/feechallan">Fee Challan</MDBNavLink>
      //             <MDBDropdownItem MDBNavLink to="feedetails">Fee Details</MDBDropdownItem>
      //             <MDBNavLink to="/feedetails">Fee Details</MDBNavLink>
      //           </MDBDropdownMenu>
      //         </MDBDropdown>
      //       </MDBNavItem>
      //       <MDBNavItem>
      //         <MDBDropdown>
      //           <MDBDropdownToggle nav caret>
      //             <span className="mr-2">Academics</span>
      //           </MDBDropdownToggle>
      //           <MDBDropdownMenu>
      //             <MDBDropdownItem MDBNavLink to="/marks">Marks</MDBDropdownItem>
      //             <MDBDropdownItem MDBNavLink to="/trancript">Transcript</MDBDropdownItem>
      //           </MDBDropdownMenu>
      //         </MDBDropdown>
      //       </MDBNavItem>
      //     </MDBNavbarNav>
      //     <MDBNavbarNav right>
      //       <MDBNavItem>
      //         <MDBNavLink to="!#">Log Out</MDBNavLink>            </MDBNavItem>
      //     </MDBNavbarNav>
      //   </MDBCollapse>
      // </MDBNavbar>

    );
  }
}

export default NavbarPage;