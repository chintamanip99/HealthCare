import React, { Component} from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import '../css/home.css';
import Menu from './menu.component'
import axios from 'axios';
import "react-datepicker/dist/react-datepicker.css";
import Loader from 'react-loader-advanced';
import { HotKeys } from "react-hotkeys";





class AppointmentForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
          "doctor":sessionStorage.getItem("doctorid"),
          "description":""
        }

     
        
    }
    componentDidMount=()=>{



        

     


        
    }

    handleSubmit = (e) => {
		e.preventDefault();
		axios.post(window.API_URL+"/appointments/appointment/0", {'patient':4, 'doctor': parseInt(sessionStorage.getItem("doctorid")), 'description': this.state.description },{'headers':{'Authorization': 'Token ' + sessionStorage.getItem('token')}})
			.then(response => {
				console.log(response)
				if (response.status == 200) {


					
					

                    alert("You have successfully sent appointment request  to the doctor ");
                        this.props.history.push('/appointments');
					
				}
				else {

					alert("You have already booked an appointment with doctor / the form is wrongly filled!");

				}
			})
			.catch(error => {

				alert("Some error occured"+error.message);
			});

	}


    handleChange = (e) => {
            this.setState({
                [e.target.name]: e.target.value
            });
        }

  render() {
   

        return (
            <HotKeys keyMap={this.keyMap} handlers={this.handlers}>
            <div className="container">
               <Loader show={this.state.loaded} message={<div class="spinner-border" role="status">
                   <span class="sr-only">Loading...</span></div>}>

                <div className="d-flex justify-content-center h-100">
                    <Menu></Menu>
                    <div style={{ maxWidth: "2000px" }} className="card float-left">

                        <div className="card-header">
                            <h3>{window.RECIEPT_MESSAGE}</h3>
                        </div>
                        <div className="col-sm-12 col-sm-offset-4 card-body">
                            <form onSubmit={this.handleSubmit} id="login_form" autoComplete="off">
                                <label style={{ color: "white" }} className="float-left" for="name"><b>Enter your health complaint</b></label>

                                <div className="input-group form-group">
                                    <input onChange={this.handleChange} type="text"  value={this.state.description} className="form-control input-sm" id="description" name="description" placeholder="Enter health complaint" required />
                                </div>
                                <div className="form-group">
									<input type="submit" value="Submit" className="btn-lg float-right login_btn" />
								</div>
                            </form>
                        </div>
                    </div>
                </div>



                </Loader>



            </div>
            </HotKeys>
            
        )
    }
}
export default AppointmentForm;
