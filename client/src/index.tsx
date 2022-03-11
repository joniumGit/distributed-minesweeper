import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './pages/homepage';
import reportWebVitals from './reportWebVitals';
import Load from './pages/load';
import FieldForm from './pages/homepage';
import MyRoutes from './routes';
import Game from './pages/game';
import Square from './pages/game';


ReactDOM.render(
  <React.StrictMode>
    <MyRoutes />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
