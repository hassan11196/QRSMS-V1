import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { Form } from 'react-bootstrap';
import axios from "axios";
import credential from './credentials.js';
import Cookies from 'js-cookie';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody, MDBSelect, MDBSelectInput, MDBSelectOptions } from 'mdbreact';

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"



class SignUp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      csrf_token: 0,
      username_admin: credential.REACT_APP_ADMIN_USERNAME,
      password_admin: credential.REACT_APP_ADMIN_PASSWORD
    }
  }
  get_csrf_token() {
    console.log("TAKING TOKEN ");

    this.setState(oldState => ({
      csrf_token: Cookies.get('csrftoken')
    }));
    this.state.csrf_token = Cookies.get('csrftoken');
    this.setState({ csrf_token: Cookies.get('csrftoken') });
  }
  componentDidMount() {
    this.get_csrf_token();
    //console.log(this.state);
    this.render();
    // console.log(this.state.csrf_token);
  }
  on_login_click = () => {
    console.log("Kaam");
    console.log(this.state);
    // console.log(this.state.csrf_token);
    // console.log(this.state);
    var formd = new FormData();
    formd.set('csrfmiddlewaretoken', this.state.csrf_token);
    formd.set('username', String(this.state.username_admin));
    formd.set('password', String(this.state.password_admin));
    formd.set('hello', 'hell');

    axios.post("/api-auth/login/", formd, {
      // username: this.state.username_admin,
      // password: this.state.password_admin,
      headers: {
        // 'X-CSRFTOKEN': this.state.csrf_token,
      },
      // auth: {
      //   username: this.state.username_admin,
      //   password: this.state.password_admin,
      // },
      params: {
        next: 'http://localhost:3000/admin/'
      },


    }
    )
      .then((response) => {
        console.log(response)
        if (response.status == 200) {
          window.location = 'http://localhost:3000/admin/';

        }
      });



  }

  
  render() {
    return (

      <MDBContainer>
        <MDBRow>
          <MDBCol>
          </MDBCol>
          <MDBCol md="5">
            <MDBCard>
              <MDBCardBody>

                <Form method='post' action='/test_student_signup'>
                  <p className="h4 text-center py-4">Sign up</p>
                  <div className="grey-text">
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.state.csrf_token}></input>
                    <MDBInput
                      autoComplete="off"
                      required
                      label="First name"
                      icon="envelope"
                      group
                      type="text"
                      validate
                      error="wrong"
                      success="right"
                      name='first_name'
                    />
                    <MDBInput
                      autoComplete="off"
                      required
                      label="Last name"
                      icon="envelope"
                      group
                      type="text"
                      validate
                      error="wrong"
                      success="right"
                      name='last_name'
                    />
                    <MDBInput
                      required
                      autoComplete="off"
                      label="Your email"
                      icon="envelope"
                      group
                      type="email"
                      validate
                      error="wrong"
                      success="right"
                      name='email'
                      type='email'
                    />
                    <MDBInput
                      required
                      autoComplete="off"
                      label="Your password"
                      icon="lock"
                      group
                      type="password"
                      validate
                      name='password'
                    />

                    <MDBInput
                      required
                      autoComplete="off"
                      name='confirm_password'
                      label="Confirm  Password"
                      icon="exclamation-triangle"
                      group
                      type="text"
                      validate
                      error="wrong"
                      success="right"
                      type="password"
                    />

                    <MDBInput
                      name='uid'
                      autoComplete="off"
                      label="Enter NU-ID"
                      icon="exclamation-triangle"
                      group
                      type="text"
                      validate
                      pattern="([0-9]{2}(K|L|I|C|P|k|l|i|c|p)-[0-9]{4})"
                      
                    />

                  </div>
                  <MDBRow>
                    <MDBCol md="6">
                      <Form.Group pattern="(20[1-9]{2})" required>
                        <Form.Label>Admission Year</Form.Label>
                        <Form.Control as="select" name='batch' >
                        
                          <option>2012</option>
                          <option>2013</option>
                          <option>2014</option>
                          <option>2015</option>
                          <option>2016</option>
                          <option>2017</option>
                          <option>2018</option>
                          <option>2019</option>
                        </Form.Control>

                      </Form.Group>


                    </MDBCol>
                    <MDBCol md="0"></MDBCol>
                    <MDBCol md="6">
                      <Form.Group >
                        <Form.Label>Gender</Form.Label>
                        <Form.Control as="select" name="gender">
                          <option>Male</option>
                          <option>Female</option>
                        </Form.Control>
                      </Form.Group>

                    </MDBCol>
                  </MDBRow>
                  <div className="text-center py-4 mt-3">
                    <MDBBtn color="cyan" type="submit" >
                      Register
                              </MDBBtn>
                  </div>
                </Form>
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
export default SignUp;