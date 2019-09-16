import React, { Component } from 'react';
import {Form, InputGroup} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import {library} from '@fortawesome/fontawesome-svg-core';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { FaCoffee } from '@fortawesome/free-solid-svg-icons';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody } from 'mdbreact';
import axios from 'axios';
class Nu_login extends Component {

  post_server_login = (e)=> {
      alert("yes");
  };


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
                    <Form.Label>Status</Form.Label>
                                 <Form.Control as="select">
                               <option>Teacher</option>
                                 <option>Student</option>
                                 </Form.Control>
                    <a href="#" className="Forget">Forget Password?</a>
                  </div>
                  <div className="text-center py-4 mt-3">
                    <MDBBtn color="cyan" type="submit" onsubmit={(e)=>{this.post_server_login(e);}}>
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
export default Nu_login;
