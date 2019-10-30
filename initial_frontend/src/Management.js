import React from 'react';
import './App.css';
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Spinner, Modal, Col, Table} from 'react-bootstrap';
import Cookies from 'js-cookie'


axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

export default class Management extends React.Component{
    
    constructor(props){
        super(props);
        this.state = {
            csrf_token:0,
            loading : false,
            modal_view : false,
            retrieved : []
        }
    }
    get_csrf_token() {
        axios.get('/get_csrf');
        this.setState(oldState => ({
          csrf_token : Cookies.get('csrftoken')
        }));
        this.setState({csrf_token : Cookies.get('csrftoken')});
      }

    componentDidMount() {
        this.get_csrf_token();
    }
    
    wrap_caller = (url) => {
        this.setState({
            loading:true,
        })
        axios.post(url).then(
            (response) => {
                console.log(response);
                if (response.data.status === 'success'){
                    let arr = []
                   for (const key in response.data) {
                       if (response.data.hasOwnProperty(key)) {
                            console.log(key + response.data[key]);
                            arr = [[key,response.data[key]], ...arr]
                       }
                   }
                   
                    this.setState({
                        retrieved : arr,
                        modal_view:true,
                    });
                }
                
            }
        ).finally(
            (response)=>{
                this.setState({
                    loading:false,
                })
            }
        );
    }
    

    add_students = ()=> {
        this.wrap_caller('/management/add_students/')
    }
    add_semesterCore = () => {
        this.wrap_caller('/management/add_semestercore/');
    }

    add_university = () => {
        this.wrap_caller('/management/add_university/');
    }
    add_superuser = () => {
        this.wrap_caller('/management/add_superuser/');
    }
    
    
    LoadingSpinner = () => (
        <div>
         <Spinner animation="border" variant="primary" /> Loading...
        </div>
      );

    setShow = (opt) => {
        
        this.setState({
            modal_view : opt,
        })
        return opt;
    };
    render (){
        

        const handleClose = () => this.setShow(false);
        const handleShow = () => this.setShow(true);
        
        return (
            
            <div>
                
                <h1>
                Management Console
            </h1>
            <Button onClick={()=>this.add_superuser()}>
                Insert Superuser
            </Button>
            <Button onClick={()=>this.add_university()}>
                Add University
            </Button>
            <Button onClick={()=>this.add_semesterCore()}>
                Add SemesterCore
            </Button>
            <Button onClick={()=>this.add_students()}>
                Insert Students
            </Button>

            {this.state.loading ? this.LoadingSpinner():<br></br>}


            <Modal show={this.state.modal_view} onHide={handleClose}>
            <Modal.Header closeButton>
              <Modal.Title>Retrieved Info</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            
            <Table>

            <tbody>
            {this.state.retrieved.map((val,key) => {
                return (
                    
                    <tr key={'row'+key}>
                        <td key={'col1'+key}>
                            {val[0]}
                        </td>
                        <td key={'col2'+key}>
                            {val[1]}
                        </td>
                    </tr>
                                        
        
                );
            })}
            </tbody>
            </Table>
            
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>

            </div>
            

            
        

        );
    };
}


