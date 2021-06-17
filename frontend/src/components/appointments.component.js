import React, { Component } from 'react'
import { MDBDataTableV5 } from 'mdbreact';
import Menu from './menu.component'
import axios from 'axios';

class Appointments extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datatable: {
        columns: [
          {
            label: 'Health Complaint',
            field: 'description',
            width: 150,
          },
          {
            label: 'Doctor\'s Prescription',
            field: 'prescription',
            width: 270,
          },
          {
            label: 'Appointment Date Time',
            field: 'datetime',
            width: 200,
          },
          {
            label: 'Meeting Link',
            field: 'meeting_link',
            width: 200,
          },
          {
            label: 'Doctor Name',
            field: 'doctor',
            width: 200,
          },
          {
            label: 'Doctor Specialization',
            field: 'doctortype',
            width: 200,
          },
        ],
        rows: [],
      }
    }

  }

  handleClick(meeting_link)
  {
    window.open(meeting_link,'_blank');

  }

  update_rows = (response) => {
    try {
      let columns = this.state.datatable.columns
      let rows = this.state.datatable.rows
      response.forEach(element => { 
        console.log(element)
        let jsonobj={"description":element.description,"prescription":element.prescription,"datetime":element.datetime,"meeting_link":element.meeting_link,"doctor":element.doctor.user.first_name+" "+element.doctor.user.last_name,"doctortype":element.doctor.doctortype.doctortype}
       
        jsonobj.clickEvent=() => this.handleClick(element.meeting_link)
        jsonobj.hover=()=>()=>{console.log("hillo")}
        console.log(jsonobj);
        rows.push(jsonobj) })
      
      let datatable = { columns: columns, rows: rows }
      this.setState({ datatable: datatable })
    }
    catch (error) {
      alert("error occurred "+error.toString())

    }
  }

  

  componentDidMount = () => {
    axios.get(window.API_URL+'/appointments/appointment/0',{ 'headers': { 'Authorization':"Token "+sessionStorage.getItem('token')  } })
      .then(response => {
        console.log(response);
        if (response.status == 200) {

            this.update_rows(response.data.data);
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
        <h1><font color="white">Appointments</font></h1>
        <div style={{ backgroundColor: "black", fontSize: "25px", color: "green" }}>
          <MDBDataTableV5 className="table-responsive" style={{ cursor: "pointer", textAlign: "left", backgroundColor: "black", fontSize: "20px", color: "white" }} hover entriesOptions={[10, 20, 25]} entries={10} pagesAmount={4} data={this.state.datatable} searchTop searchBottom={false} />
        </div>
      </div>

    )

  }
}
export default Appointments;