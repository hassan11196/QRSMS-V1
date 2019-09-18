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

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

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

    const token = axios.get("/get_csrf")
      .then((response) => {
        // console.log(response);
        // this.state.csrf_token = response.data.csrfToken;
        this.state.csrf_token = Cookies.get('csrftoken');
        // console.log(this.state.csrf_token);
        return response.data.csrfToken;
      });


  }

  componentDidMount() {
    this.get_csrf_token();
    // console.log(this.state.csrf_token);
  }
  on_login_click = () => {
    // console.log(this.state.csrf_token);
    // console.log(this.state);
    var formd = new FormData();
    formd.set('username', String( this.state.username_admin));
    formd.set('password', String(this.state.password_admin));
    formd.set('hello','hell');
    // console.log(formd);
    axios.post("/api-auth/login/", {
      username:this.state.username_admin,
      password:this.state.password_admin,
      headers: {
        'X-CSRFTOKEN': this.state.csrf_token,
        'Content-Type': 'multipart/form-data', 
      },
      data: formd,
      
    }
    )
      .then((response) => {
        // console.log(response)
      });

  }


  render() {
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
                <form>
                  <p className="h4 text-center py-4">Sign In</p>
                  <div className="text-center">
                    <MDBInput
                      label="ID i.e k173650"
                      icon="envelope"
                      group
                      type="text"
                      validate
                      error="wrong"
                      success="right"
                    />
                    <MDBInput
                      label="Password"
                      icon="lock"
                      group
                      type="password"
                      validate
                    />
                    <a href="#" className="Forget">Forget Password?</a>
                  </div>
                  <div className="text-center py-4 mt-3">
                    <MDBBtn color="cyan" type="submit" >
                      Login
                    </MDBBtn>
                    <MDBBtn onClick={()=>this.on_login_click()}>
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
