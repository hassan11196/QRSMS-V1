import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import './App.css';
import 'mdbreact/dist/css/mdb.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { FaCoffee } from '@fortawesome/free-solid-svg-icons';
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn, MDBCard, MDBCardBody } from 'mdbreact';
import { Card } from 'react-bootstrap';
import { CardBody } from 'react-bootstrap/Card';

var data = {
    name:"Muhammad"
};



class AhsanHome extends Component {


    render() {
        return (

            <MDBContainer>
                <br />
                <MDBRow>

                    <MDBCol>
                        <Card>
                            <Card.Body>
                                <Card.Title style={{ fontWeight: "bold", background: "dodgerblue", color: "white" }}>Personal Information</Card.Title>
                                <Card.Text style={{ textAlign: "left" }}>
                                    <MDBRow>
                                        <MDBCol md="4">
                                            <span style={{ fontWeight: "bold" }}>Name: </span><span>{data.name}</span>
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


                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>

                <br />


                <MDBRow>

                    <MDBCol>
                        <Card>
                            <Card.Body>
                                <Card.Title style={{ fontWeight: "bold", background: "dodgerblue", color: "white" }}>University Information</Card.Title>

                                <Card.Text style={{ textAlign: "left" }}>
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


                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>



                <br />



                <MDBRow>
                    <MDBCol>
                        <Card>
                            <Card.Body>
                                <Card.Title style={{ fontWeight: "bold", background: "dodgerblue", color: "white" }}>Contact Information</Card.Title>
                                <Card.Text style={{ textAlign: "left" }}>
                                    <MDBRow>
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
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        );
    }
}
export default AhsanHome;