import { Link } from "react-router-dom"

export default function Navbar(){

  return (

    <div className="bg-black text-white p-4 flex gap-6">

      <Link to="/">Dashboard</Link>

      <Link to="/projects">Projects</Link>

      <Link to="/endpoints">Endpoints</Link>

      <Link to="/monitoring">Monitoring</Link>

      <Link to="/alerts">Alerts</Link>

      <Link to="/login">Login</Link>

    </div>

  )

}