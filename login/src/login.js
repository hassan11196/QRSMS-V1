import React, { Component } from 'react';
import {Fabeer} from 'react-icons/fa';
import 'bootstrap/dist/css/bootstrap.min.css';
import {library} from '@fortawesome/fontawesome-svg-core';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { FaCoffee } from '@fortawesome/free-solid-svg-icons';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody } from 'mdbreact';
class Login extends Component {
  render(){
    return (    
    <MDBContainer>
        <MDBRow>
        <p>     </p>
        </MDBRow>
        <br/><br/><br/>
          <MDBRow>
              <MDBCol md="4">
              </MDBCol>
          <MDBCol md="4">
            <MDBCard className ="card text-center">
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
                    <MDBBtn color="cyan" type="submit">
                      Login
                    </MDBBtn>
                  </div>
                </form>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
          <br/><br/><br/>
          
        </MDBRow>
      </MDBContainer>
  );
}
}
export default Login;
