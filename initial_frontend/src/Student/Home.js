import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaHome, FaUser, FaBookReader } from "react-icons/fa";
import './home.css';
import 'mdbreact/dist/css/mdb.css';
import { MDBRow, MDBCol } from 'mdbreact';
import { Card, Container, ProgressBar } from 'react-bootstrap';
import NavbarPage from './NavBar';
class Home extends Component {
    render() {
        return (
            
            <Container bsPrefix="cont">
                <NavbarPage/>
                <br />
                <br />
                <br />
                <h5 style={{ textAlign: "left" }}><span style={{ fontWeight: "bold", color: "black" }}>Home</span> <span>| Information</span></h5>
                <MDBRow>

                    <MDBCol>
                        <Card>
                            <Card.Body className="headingBody">
                                <Card.Title as="h4" ><span className="toggleiconHeight"><FaHome /></span>
                                    <span className="toggletextSize">Personal Information</span></Card.Title>
                            </Card.Body>
                            <Card.Body className="textBody" style={{ textAlign: "left" }}>
                               
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Name: </span><span>Muhammad Ahsan Siddiq</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Father Name: </span><span>Muhammad Ali</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Gender: </span><span>Male</span>
                                        </MDBCol>
                                    </MDBRow>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>DOB: </span><span>21/08/1999</span>
                                        </MDBCol>
                                        <MDBCol md="4" >
                                            <span style={{ fontWeight: "bold" }}>Blood Group: </span><span>O+</span>
                                        </MDBCol>
                                        <MDBCol>
                                            <span style={{ fontWeight: "bold" }}>CNIC: </span><span></span>
                                        </MDBCol>
                                    </MDBRow>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Nationality: </span><span>Pakistan</span>
                                        </MDBCol>
                                        <MDBCol >
                                            <span style={{ fontWeight: "bold" }}>Mobile No: </span><span>0348222460</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Email: </span><span>muhammmad.aichee@gmail.com</span>
                                        </MDBCol>
                                    </MDBRow>


                               
                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>

                <br />


                <MDBRow>

                    <MDBCol>
                        <Card>
                            <Card.Body className="headingBody">
                                <Card.Title as="h4" ><span className="toggleiconHeight"><FaBookReader /></span>
                                    <span className="toggletextSize">University Information</span></Card.Title>
                            </Card.Body>
                            <Card.Body className="textBody" style={{ textAlign: "left" }}>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Roll No: </span><span>17K-3650</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Campus: </span><span>Karachi</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Degree: </span><span>BS(CS)</span>
                                        </MDBCol>
                                    </MDBRow>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Batch: </span><span>2017</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Status: </span><span>Current</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Semester: </span><span>Fall</span>
                                        </MDBCol>
                                    </MDBRow>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Nationality: </span><span>Pakistan</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Mobile No: </span><span>0348222460</span>
                                        </MDBCol>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Email: </span><span>muhammmad.aichee@gmail.com</span>
                                        </MDBCol>
                                    </MDBRow>


                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>



                <br />



                <MDBRow>
                    <MDBCol>
                        <Card>
                            <Card.Body className="headingBody">
                                <Card.Title as="h4" ><span className="toggleiconHeight"><FaUser /></span>
                                    <span className="toggletextSize">Contact Information</span></Card.Title>
                            </Card.Body>
                            <Card.Body className="textBody" style={{ textAlign: "left" }}>                                    <MDBRow>
                                    <MDBCol md="5">
                                        <span style={{ fontWeight: "bold" }}>Address: </span><span>P/No. B-90, Block No. 3/A Gulistan-E-Johar</span>
                                    </MDBCol>
                                    <MDBCol md="5">
                                        <span style={{ fontWeight: "bold" }}>Home Phone: </span><span> 0321-2056627 </span>
                                    </MDBCol>
                                </MDBRow>
                                <MDBRow>
                                    <MDBCol md="5">
                                        <span style={{ fontWeight: "bold" }}>City: </span><span>Karachi</span>
                                    </MDBCol>
                                    <MDBCol >
                                        <span style={{ fontWeight: "bold" }}>Country: </span><span>Pakistan</span>
                                    </MDBCol>
                                </MDBRow>
                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>



                <br />


                <MDBRow>
                    <MDBCol>
                        <Card>
                        <Card.Body className="headingBody">
                               <Card.Title as="h4" ><span className="toggleiconHeight"><FaBookReader/></span>
                                <span className="toggletextSize">Attendance</span></Card.Title> 
                            </Card.Body>
                            <Card.Body className="textBody">                                  <div>
                                    <ProgressBar striped variant="success" now={40} /><br/>
                                    <ProgressBar striped variant="info" now={20} /> <br/>
                                    <ProgressBar striped variant="warning" now={60} /><br/>
                                    <ProgressBar striped variant="danger" now={80} /><br/>
                                </div>    
                            </Card.Body> 
                        </Card>
                    </MDBCol>
                </MDBRow>
     

            </Container>
        );
    }
}
export default Home;