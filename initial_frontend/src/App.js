import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card} from 'react-bootstrap';
import credential from './credentials.js';

class CourseView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      courses_fetched: [],
      fetch_staus: true,
      page:0
    }
  }
  componentDidMount() {
    let username_admin = credential.REACT_APP_ADMIN_USERNAME;
    let password_admin = credential.REACT_APP_ADMIN_PASSWORD;
    console.log(username_admin + password_admin);
    axios.get("course_info/",{
      auth: {
        username: username_admin,
        password: password_admin,
      },
      params : {
        page:1
      }
    })
      .then(
        (response) => {
          this.setState(oldState => ({
            courses_fetched: response.data.results,
            fetch_staus: true,
            page:1
          }));
          console.log(response.data);
                   return;
        }
      );
  }

  next_course_page(){

    console.log("Current Page : " + this.state.page);
    if(this.state.page === 5){
      return;
    }

    let username_admin = credential.REACT_APP_ADMIN_USERNAME;
    let password_admin = credential.REACT_APP_ADMIN_PASSWORD;
  


    axios.get("course_info/",{
      auth: {
        username: username_admin ,
        password: password_admin,
      },
      params : {
        page:this.state.page + 1
      }
    })
      .then(
        (response) => {
          this.setState(oldState => ({
            courses_fetched: response.data.results,
            fetch_staus: true,
            page:oldState.page + 1
          }));
          
        }
      );
  }

  render() {
   
    return (
      
      <div className="container">
        <h1> Courses </h1>
        <div >
        <Button variant="secondary" onClick={() => this.next_course_page()}>Next Course Page</Button>
          <div>
            {
              this.state.courses_fetched ? this.state.courses_fetched.map((c) => {
                return (
                  this.course_box(c)
                );
              }) : <h2> Cant Fetch Courses </h2>
            }
          </div>
        </div>
          
      </div>
    );
  }

  course_box(course_obj){
    return (
      <li key={ "list_key" + course_obj.course_code}>
        <Card>
          <Card.Body>
            <Card.Title>
            {course_obj.course_name}
            </Card.Title>
            <Card.Subtitle>
            {course_obj.course_short}
            </Card.Subtitle>
            <Card.Text>
            {course_obj.course_code}
            </Card.Text>
          </Card.Body>
        </Card>
      </li>
    );
  }

}

function App() {
  return (
    <div className="App">
      <CourseView />
    </div>
    

  );
}

export default App;
