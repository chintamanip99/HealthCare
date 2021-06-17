import React, { Component } from 'react'
import { MDBDataTableV5 } from 'mdbreact';
import Menu from './menu.component'
import axios from 'axios';

class Doctors extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datatable: {
        columns: [
          {
            label: 'First Name',
            field: 'first_name',
            width: 150,
          },

          {
            label: 'Last Name',
            field: 'last_name',
            width: 270,
          },
          {
            label: 'Email',
            field: 'email',
            width: 300,
          },
          {
            label: 'Doctor Type',
            field: 'doctortype',
            width: 270,
          },
          {
            label: 'Phone Number',
            field: 'phone',
            width: 270,
          },
          {
            label: 'Description',
            field: 'description',
            width: 1000,
          },
          {
            label: 'Book Appointment',
            field: 'linktobook',
            width: 150,
          },
          
          

        ],
        rows: [],
      }
    }

  }

  handleClick=(doctorid)=>
  {
    console.log("hjhjuuuuuuuuuuuuuuuu");
    sessionStorage.setItem('doctorid',doctorid);
    this.props.history.push('/appointmentform');

  }

  update_rows = (response) => {
    try {
      let columns = this.state.datatable.columns
      let rows = this.state.datatable.rows
      response.forEach(element => { 
        let jsonobj={"email":element.user.email,"first_name":element.user.first_name,"last_name":element.user.last_name,"doctortype":element.doctortype.doctortype,"phone":element.phone,"description":element.description,"linktobook":"Book Appointment"}
        console.log(element)
        jsonobj.clickEvent=() => this.handleClick(element.user.id)
        element.hover=()=>()=>{console.log("hillo")}
        console.log(element);
        rows.push(jsonobj) })
      
      let datatable = { columns: columns, rows: rows }
      this.setState({ datatable: datatable })
    }
    catch (error) {
      alert("error occurred "+error.toString())

    }
  }

  

  componentDidMount = () => {
    axios.get(window.API_URL+'/profiles/doctors/',{ 'headers': { 'Authorization':"Token "+sessionStorage.getItem('token')  } })
      .then(response => {
        console.log(response);
        if (response.status == 200) {

            this.update_rows(response.data.results);
          }
          else {
            alert(response.error.error.toString()+" Unknown Error Occurred")
          }
        }
      )
      .catch(error => {
        alert("error occurred "+error.toString())
      });
  }


  render() {

    return (
      <div>
        <Menu />
        <h1><font color="white">Doctors</font></h1>
        <div style={{ backgroundColor: "black", fontSize: "25px", color: "green" }}>
          <MDBDataTableV5 className="table-responsive" style={{ cursor: "pointer", textAlign: "left", backgroundColor: "black", fontSize: "20px", color: "white" }} hover entriesOptions={[10, 20, 25]} entries={10} pagesAmount={4} data={this.state.datatable} searchTop searchBottom={false} />
        </div>
      </div>

    )

  }
}
export default Doctors;