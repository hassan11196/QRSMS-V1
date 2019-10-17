import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import Qrsms from './Qrsms'


if(document.body.contains(document.getElementById('DApp'))){
    ReactDOM.render(<Qrsms/>, document.getElementById('DApp'));
    console.log("In Django Environment");
}
else{
    ReactDOM.render(<Qrsms/>, document.getElementById('root'));
    console.log("In Local Environment");
}

// ReactDOM.render(<Login/>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
