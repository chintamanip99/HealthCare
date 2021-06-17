import React,{Component} from 'react'
import '../css/menu.css';
import { NavLink } from 'react-router-dom';


class Menu extends Component
{
constructor(props)
{
    super(props);
    this.state={
        width:"0%"
    }
}
openNav=()=>{
    this.setState({
        width:"100%"
    })
}
closeNav=()=>{
    this.setState({
        width:"0%"
    })
}

render()
{
    return(
        <div style={{float:"left"}}>
            <div style={{width:this.state.width}} id="myNav" className="overlay">
  <a href="#" className="closebtn" onClick={this.closeNav}>&times;</a>
  <div className="overlay-content">
    <NavLink to="/appointments">Appointments</NavLink>
    <NavLink to="/doctors">Doctors</NavLink>
  </div>
</div>
<span style={{fontSize:"40px",cursor:"pointer",color:"white"}} onClick={this.openNav}>&#9776;</span>
 </div>
    )
}
}
export default(Menu)