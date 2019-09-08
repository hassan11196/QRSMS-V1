import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';


if(document.body.contains(document.getElementById('DApp'))){
    ReactDOM.render(<App />, document.getElementById('DApp'));
}
else{
    ReactDOM.render(<App />, document.getElementById('root'));
    console.log("In Local Environment");
}
// 

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
