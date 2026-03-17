import { useState, useContext } from "react"
import { useNavigate } from "react-router-dom"

import API from "../services/api"
import { AuthContext } from "../context/AuthContext"

export default function Login(){

  const [email,setEmail]=useState("")
  const [password,setPassword]=useState("")

  const { login } = useContext(AuthContext)

  const navigate = useNavigate()

  const handleSubmit = async (e) => {

    e.preventDefault()

    try{

      const res = await API.post("/auth/login",{
        email,
        password
      })

      login(res.data.token)

      navigate("/")

    }
    catch(err){

      alert("Login failed")

    }

  }

  return(

    <div className="p-6">

      <h1 className="text-xl font-bold mb-4">
        Login
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
          Login
        </button>

      </form>

    </div>

  )

}