import React, { Component } from 'react'
import { BrowserRouter, Route, NavLink, Link, Switch } from 'react-router-dom'

import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody, MDBNav } from 'mdbreact';
import 'mdbreact/dist/css/mdb.css';

import Login from './login';
import AhsanHome from './AhsanHome';
import SignUp from './signup';

class Qrsms extends Component {
    render() {
        return (
            <div className="App">

                <BrowserRouter>
                    <Switch>
                        <Route exact path='/' component={StudentHome} />
                        <Route path='/shome' component={AhsanHome} />
                        <Route exact path='/login' component={() => <Login user="Admin" />} />
                        <Route path='/login/student' component={() => <Login user="Student" />}></Route>
                        <Route path='/signup' component={SignUp}></Route>
                        {/* <Route path='/admin'component={() => {window.location.href = 'proxy://admin'}} ></Route> */}
                        <Route component={PageNotFound}></Route>
                    </Switch>

                </BrowserRouter>

            </div>
        );

    }
}

class PageNotFound extends Component {
    render() {
        return (
            <h1>Error 404 - PageNotFound</h1>
        );
    }
}

class StudentHome extends Component {
    render() {
        return (
            <div className="App">
                <h1>Student Portal - Debugging Buttons</h1>
                <nav>
                    <NavLink to='/signup' >
                        <MDBBtn color="white">
                            Signup
                        </MDBBtn>
                    </NavLink>
                    <NavLink to='/login/student' >
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