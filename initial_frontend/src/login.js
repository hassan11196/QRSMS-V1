import React, { Component } from 'react';
import { Fabeer } from 'react-icons/fa';
import 'bootstrap/dist/css/bootstrap.min.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { FaCoffee } from '@fortawesome/free-solid-svg-icons';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody } from 'mdbreact';
import axios from "axios";
import credential from './credentials.js';
import Cookies from 'js-cookie';
import { Redirect } from 'react-router-dom';


axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"


class Home extends Component{
  render(){
    return (
      <h1>
        Home
      </h1>
    );
  }
}

class Login extends Component {


  constructor(props) {
    super(props);
    this.state = {
      csrf_token: 0,
      username_admin: credential.REACT_APP_ADMIN_USERNAME,
      password_admin: credential.REACT_APP_ADMIN_PASSWORD
    }
  }

  get_csrf_token() {
    //console.log("TAKING TOKEN ");
    
    this.setState(oldState => ({
      csrf_token : Cookies.get('csrftoken')
    }));
    this.state.csrf_token = Cookies.get('csrftoken');
    this.setState({csrf_token : Cookies.get('csrftoken')});
    //console.log(this.state);
    // const token = axios.get("/get_csrf")
    //   .then((response) => {
    //     // console.log(response);
    //     // this.state.csrf_token = response.data.csrfToken;
    //     this.state.csrf_token = Cookies.get('csrftoken');
    //     // console.log(this.state.csrf_token);
    //     return response.data.csrfToken;
    //   });


  }

  componentDidMount() {
    this.get_csrf_token();
    //console.log(this.state);
    this.render();
    // console.log(this.state.csrf_token);
  }
  on_login_click = () => {
    console.log(this.state);
    // console.log(this.state.csrf_token);
    // console.log(this.state);
    var formd = new FormData();
    formd.set('csrfmiddlewaretoken',this.state.csrf_token);
    formd.set('username', String(this.state.username_admin));
    formd.set('password', String(this.state.password_admin));
    formd.set('hello', 'hell');
    // console.log(formd);
    axios.post("/api-auth/login/",formd, {
      // username: this.state.username_admin,
      // password: this.state.password_admin,
      headers: {
        // 'X-CSRFTOKEN': this.state.csrf_token,
      },
      // auth: {
      //   username: this.state.username_admin,
      //   password: this.state.password_admin,
      // },
      params:{
        next:'http://localhost:8000/admin/'
      },


    }
    )
      .then((response) => {
        console.log(response)
        // Some things feel so wrong, yet work so well. This is one of those things.
        if (response.status == 200){
          window.location = 'http://localhost:8000/admin/';
          
        }
      });

      

  }


  render() {
    //console.log("Render");
    return (
      <MDBContainer>
        <MDBRow>
          <p>     </p>
        </MDBRow>
        <br /><br /><br />
        <MDBRow>
          <MDBCol md="4">
          </MDBCol>
          <MDBCol md="4">
            <MDBCard className="card text-center">
              <MDBCardBody>
    
                <form method="post" action="/api-auth/login/?next=http://localhost:8000/admin">
                  <p className="h4 text-center py-4">Sign In</p>
                  <div className="text-center">
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.state.csrf_token}></input>
                    <MDBInput
                      label="ID i.e k173650"
                      icon="envelope"
                      group
                      type="text"
                      validate
                      error="wrong"
                      success="right"
                      name='username'
                    />
                    <MDBInput
                      label="Password"
                      icon="lock"
                      group
                      type="password"
                      validate
                      name="password"
                    />
                    <a href="#" className="Forget">Forget Password?</a>
                  </div>
                  <div className="text-center py-4 mt-3">
                    <MDBBtn color="cyan" type="submit" >
                      Login
                    </MDBBtn>
                    <MDBBtn onClick={() => this.on_login_click()}>
                      AZAB
                    </MDBBtn>
                  </div>
                </form>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
          <br /><br /><br />

        </MDBRow>
      </MDBContainer>
    );
  }
}
export default Login;
