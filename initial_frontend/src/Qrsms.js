import React, { Component } from 'react'
import { BrowserRouter, Route, NavLink } from 'react-router-dom'

import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody, MDBNav } from 'mdbreact';
import 'mdbreact/dist/css/mdb.css';

import Login from './login';
import AhsanHome from './AhsanHome';

class Qrsms extends Component {
    render() {
        return (
            <div className="App">

                <BrowserRouter>
                    <Route path='/' component={StudentHome} />
                    <Route path='/shome' component={AhsanHome} />
                    <Route path='/login' component={Login} />
                </BrowserRouter>

            </div>
        );

    }
}

class StudentHome extends Component {
    render() {
        return (
            <div className="App">
                <h1>Student Portal</h1>
                <nav>
                    <NavLink to='/login' >
                        <MDBBtn color="white">
                            Login
                        </MDBBtn>
                    </NavLink>

                    <br></br>

                    <NavLink to='/shome'>
                        <MDBBtn color="white">
                            Ahsans Home
                        </MDBBtn>
                    </NavLink>
                </nav>
             






            </div>
        );
    }
}

export default Qrsms;