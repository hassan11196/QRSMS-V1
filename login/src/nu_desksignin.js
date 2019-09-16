import React, { Component } from 'react';
import {FaBeer} from 'react-icons/fa';
import 'bootstrap/dist/css/bootstrap.min.css';
import {library} from '@fortawesome/fontawesome-svg-core';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import{ Form } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { FaCoffee } from '@fortawesome/free-solid-svg-icons';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody } from 'mdbreact';
class Nu_desksignin extends Component
{
    render(){
        return(
         
                <MDBContainer>
                    
                    <br></br>
                  <MDBRow>
                      <MDBCol>
                          </MDBCol>
                    <MDBCol md="5">
                      <MDBCard>
                        <MDBCardBody>
                          <form>
                            <p className="h4 text-center py-4">Sign up</p>
                            <div className="grey-text">
                              <MDBInput
                                label="Your name"
                                icon={<FaBeer/>}
                                group
                                type="text"
                                validate
                                error="wrong"
                                success="right"
                              />
                              
                              <MDBInput
                                label="Your email"
                                icon="envelope"
                                group
                                type="email"
                                validate
                                error="wrong"
                                success="right"
                              />
                              <MDBRow>
                              <MDBCol md='6'>
                              <MDBInput
                                label="Your password"
                                icon="lock"
                                group
                                type="password"
                                validate
                              />
                              </MDBCol>
                              <MDBCol md='6'>
                              <MDBInput
                                label="Confirm  Password"
                                icon="exclamation-triangle"
                                group
                                type="text"
                                validate
                                error="wrong"
                                success="right"
                              />
                              </MDBCol>
                              </MDBRow>
                              </div>
                              <MDBRow>
                              <MDBCol md= '6'>
                              <MDBInput
                                label="Your Batch"
                                icon="user"
                                group
                                type="text"
                                validate
                                error="wrong"
                                success="right"
                              />
                              </MDBCol>
                              <MDBCol md='6'>
                              <Form.Label>Status</Form.Label>
                                 <Form.Control as="select">
                               <option>Teacher</option>
                                 <option>Student</option>
                                 </Form.Control>
                                 </MDBCol>
                                 </MDBRow>
                            <div className="text-center py-4 mt-3">
                              <MDBBtn color="cyan" type="submit">
                                Register
                              </MDBBtn>
                            </div>
                          </form>
                        </MDBCardBody>
                      </MDBCard>
                    </MDBCol>
                    <MDBCol>
                          </MDBCol>
                  </MDBRow>
                </MDBContainer>
        );
    }
}
export default Nu_desksignin;