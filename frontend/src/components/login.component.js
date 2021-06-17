import React, { Component } from 'react';
import md5 from 'md5-hash';
import '../css/login.css';
import axios from 'axios';
class Login extends Component {
	constructor(props) {
		super(props)
		sessionStorage.clear()
		this.state = {
			username: null,
			password: null,
			password2: null,
			age:null,
			email:null,
			phone:null,
			first_name:null,
			last_name:null,
			birthdate:null,
			gender:null,
			address:null,
			isLoggedIn: false,
			errors: [],

		}
	}

	handleChange = (e) => {
		this.setState({
			[e.target.name]: e.target.value
		})
	}

	errorOccured = (status, err, message) => {
		let error = { "id": this.state.errors.length + 1, "status": status, "error": err, "message": message }
		let errors = this.state.errors
		errors.push(error)

		this.setState(errors)
	}

	deleteError = (e) => {
		let key = e.currentTarget.parentNode.getAttribute("data-key");

		let errors = this.state.errors.filter(error => {
			return parseInt(error.id) !== parseInt(key);
		})
		this.setState({ errors: errors })
	}




	handleSubmit = (e) => {
		e.preventDefault();
		axios.post(window.API_URL+"/profiles/login_user/", { 'username': this.state.username, 'password': this.state.password })
			.then(response => {
				console.log(response)
				if (response.status == 200) {
					console.log("hhhh");

					if (response.data.status == 404) {


						this.errorOccured(404, response.data.error.error, "Invalid Username or Password")
					}
					else {
						
						
						this.setState({ isLoggedIn: true, error: false })
						sessionStorage.setItem('token', response.data.token);
						this.props.history.push('/appointments');
					}
				}
				else {

					this.errorOccured(500, "erro occurred", "Unknown error occurred")

				}
			})
			.catch(error => {

				this.errorOccured(500, "error occurred", error.message)
			});

	}

	handleSubmit1 = (e) => {
		e.preventDefault();
		axios.post(window.API_URL+"/profiles/register_patient/", 
		{ 
		'username': this.state.username, 
		'password': this.state.password,
		'password2': this.state.password2,
		'age':this.state.age,
		'email':this.state.email,
		'phone':this.state.phone,
		'first_name':this.state.first_name,
		'last_name':this.state.last_name,
		'birthdate':this.state.birthdate,
		'gender':this.state.gender,
		'address':this.state.address,
		 })
			.then(response => {
				console.log("response is");
				console.log(response);
				if (response.status == 200) {
					console.log("response.data");
					console.log(response.data.username[0]);

					 if(response.data.token){
						
						alert("Patient Sign Up successful, login to proceed");
						this.props.history.push('/');
					}
					else if(response.data.username){
						console.log("Username: "+response.data.username[0]);
						alert("Username: "+response.data.username[0]);
					  };
					  if(response.data.email){
						alert(response.data.email);
						if(response.data.email[0].length>1){
						alert("Email: "+response.data.email[0]);
						};
					  }
					  else  if(response.data.password){
						alert("Password: "+response.data.password);
						if(response.data.password[0].length>1){
						  alert("Password: "+response.data.password[0]);
						}
					  }
					  else if(response.data.password2){
						if(response.password[0].length>1){
						  alert("Password: "+response.data.password2[0]);
						}
					  }
					  else  if(response.data.age){
						alert("Age: "+response.data.age);
					  }
					  else  if(response.data.phone){
						alert("Phone Number: "+response.data.phone[0]);
					  }
					  else  if(response.data.first_name){
						alert("First Name: "+response.data.first_name[0]);
					  }
					  else  if(response.data.last_name){
						alert("Last Name: "+response.data.last_name[0]);
					  }
					  else  if(response.data.birthdate){
						alert("Birthdate: "+response.data.birthdate[0]);
					  }
					  else  if(response.data.gender){
						alert("Gender: "+response.data.gender[0]);
					  }
					  else  if(response.data.address){
						alert("Address: "+response.data.address[0]);
					  }
				}
				else {

					this.errorOccured(500, "erro occurred", "Unknown error occurred");
					alert("only 65+ age is allowed");

				}
			})
			.catch(error => {

				this.errorOccured(500, "Please Fill the form correctly (age should be above 65+)","");
			});

	}

	render() {
		var Error = this.state.errors.length ? this.state.errors.map(error => {
			return (<div data-key={error.id} className='alert alert-danger alert-dismissible'>
				<a href="#" onClick={this.deleteError} class="close" data-dismiss="alert" aria-label="close">&times;</a>
				<div><strong>error!</strong> {error.error}</div>
				<div><strong>message</strong> {error.message}</div>
				<div><strong>status</strong> {error.status}</div></div>)
		}) : ("")



		return (
			<div className="container">
				{Error}
				<div className="d-flex justify-content-center h-100">
					<div className="card">
						<div className="card-header">
							<h3>{window.SIGN_IN_MESSAGE}</h3>
						</div>
						<div className="card-body">
							<form onSubmit={this.handleSubmit} id="login_form">
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-user"></i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="username" name="username" placeholder="username" required></input>

								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-key"></i></span>
									</div>
									<input onChange={this.handleChange} type="password" className="form-control" id="password" name="password" placeholder="password" required></input>
								</div>
								<div className="form-group">
									<input type="submit" value="Login" className="btn-lg float-right login_btn" />
								</div>
							</form>
							<form  id="login_form1">
								<button>
							<a target="blank" href={window.API_URL+'/admin/'}>Doctor Login</a>
							</button>
							</form>

						</div>
					</div>
				</div>

				<div className="d-flex justify-content-center h-100">
					<div className="card">
						<div className="card-header">
							<h3>{window.SIGN_UP_MESSAGE}</h3>
						</div>
						<div className="card-body">
							<form onSubmit={this.handleSubmit1} id="login_form">
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-user"></i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="username" name="username" placeholder="username" required></input>

								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-key"></i></span>
									</div>
									<input onChange={this.handleChange} type="password" className="form-control" id="password" name="password" placeholder="password" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-key"></i></span>
									</div>
									<input onChange={this.handleChange} type="password" className="form-control" id="password1" name="password2" placeholder="password again" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Email</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password12" name="email" placeholder="email" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>First Name</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password2" name="first_name" placeholder="first name" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Last Name</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password3" name="last_name" placeholder="last name" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Age</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password4" name="age" placeholder="age" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Birth Date</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password4" name="birthdate" placeholder="birth date" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Gender</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password5" name="gender" placeholder="gender" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Address</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password13" name="address" placeholder="address" required></input>
								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i>Phone Number</i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="password136" name="phone" placeholder="phone number" required></input>
								</div>
								<div className="form-group">
									<input type="submit" value="Sign Up" className="btn-lg float-right login_btn" />
								</div>
							</form>

						</div>
					</div>
				</div>
			</div>
		)
	}
}
export default Login;