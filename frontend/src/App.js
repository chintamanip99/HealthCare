import React from 'react';
import './App.css';
import Menu from './components/menu.component.js';
import Login from './components/login.component.js';
import Doctors from './components/doctors.component.js';
import Appointments from './components/appointments.component';
import AppointmentForm from './components/appointmentform.component';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter,Route,Switch, Router} from 'react-router-dom';

import { HotKeys } from "react-hotkeys";


function App() {
  return (
   
    <BrowserRouter>
    <div className="App">
     <Route exact path='/menu' component={Menu}></Route>
     <Route exact path='/appointments' component={Appointments}></Route>
     <Route exact path='/doctors' component={Doctors}></Route>
     <Route exact path='/appointmentform' component={AppointmentForm}></Route>
     <Route exact path='/' component={Login}></Route>

    </div>
    </BrowserRouter>
    
  );
}

export default App;
