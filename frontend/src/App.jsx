import { Routes, Route } from "react-router-dom"

import Navbar from "./components/Navbar"
import ProtectedRoute from "./components/ProtectedRoute"

import Dashboard from "./pages/Dashboard"
import Projects from "./pages/Projects"
import Endpoints from "./pages/Endpoints"
import Monitoring from "./pages/Monitoring"
import Alerts from "./pages/Alerts"
import Login from "./pages/Login"
import Register from "./pages/Register"

export default function App(){

  return(

    <div>

      <Navbar/>

      <Routes>

        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>

        <Route path="/"
          element={
            <ProtectedRoute>
              <Dashboard/>
            </ProtectedRoute>
          }
        />

        <Route path="/projects"
          element={
            <ProtectedRoute>
              <Projects/>
            </ProtectedRoute>
          }
        />

        <Route path="/endpoints"
          element={
            <ProtectedRoute>
              <Endpoints/>
            </ProtectedRoute>
          }
        />

        <Route path="/monitoring"
          element={
            <ProtectedRoute>
              <Monitoring/>
            </ProtectedRoute>
          }
        />

        <Route path="/alerts"
          element={
            <ProtectedRoute>
              <Alerts/>
            </ProtectedRoute>
          }
        />

      </Routes>

    </div>

  )

}