import React, { Component } from 'react'
import { BrowserRouter, Route, NavLink, Link, Switch } from 'react-router-dom'
import {Button} from 'react-bootstrap';
import {createStore} from 'redux';

import Login from './Student/login';
import Home from './Student/Home';
import SignUp from './Student/Signup';
import CourseView from './CourseView';
import NavBar from './Student/NavBar';
import Management from './Management.js';
import Axios from 'axios';



class Shome extends Component{
    constructor(props){
        super(props);
        this.state = {
            home_json : {}
        }
    }
    componentDidMount() {
        Axios.get('/student/home_json/').then(
            (response) => {
                this.setState({
                    home_json:response.data
                })
                console.log(this.state.home_json);
            }
        );
    }
    
    render(){
        return(
            <div>
                check console
            </div>
        );
    }
}
class Qrsms extends Component {
    render() {
        return (
            <div className="App">

                <BrowserRouter>
                    <Switch>
                        <Route exact path='/' component={StudentHome} />
                        <Route path ='/Management' component={Management}></Route>
                        <Route path='/home' component={Home} />
                        <Route exact path='/login' component={() => <Login user="Admin" />} />
                        <Route path='/login' component={() => <Login user="Student" />}></Route>
                        <Route path='/signup' component={SignUp}></Route>
                        {/* <Route path='/admin'component={() => {window.location.href = 'proxy://admin'}} ></Route> */}
                        <Route path='/course' component={CourseView}></Route>
                        <Route path='/shome' component={Shome}></Route>
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
                        <Button color="white">
                            Signup
                        </Button>
                    </NavLink>
                    <NavLink to='/login/student' >
                        <Button color="white">
                            Login
                        </Button>
                    </NavLink>

                    <br></br>

                    <NavLink to='/shome'>
                        <Button color="white">
                            Ahsans Home
                        </Button>
                    </NavLink>
                    <NavLink to='/Management' >
                        <Button color="white">
                            Management
                        </Button>
                    </NavLink>
                </nav>
            </div>
        );
    }
}

export default Qrsms;