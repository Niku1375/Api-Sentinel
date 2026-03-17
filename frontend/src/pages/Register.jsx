import { useState } from "react"
import { useNavigate } from "react-router-dom"

import API from "../services/api"

export default function Register(){

  const [email,setEmail]=useState("")
  const [password,setPassword]=useState("")

  const navigate = useNavigate()

  const handleSubmit = async (e)=>{

    e.preventDefault()

    try{

      await API.post("/auth/register",{
        email,
        password
      })

      alert("Account created")

      navigate("/login")

    }
    catch(err){

      alert("Registration failed")

    }

  }

  return(

    <div className="p-6">

      <h1 className="text-xl font-bold mb-4">
        Register
      </h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3 w-80">

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          className="border p-2"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          className="border p-2"
        />

        <button className="bg-black text-white p-2">
          Register
        </button>

      </form>

    </div>

  )

}