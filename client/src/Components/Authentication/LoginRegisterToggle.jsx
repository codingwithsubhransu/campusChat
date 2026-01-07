import React from 'react'
import { NavLink } from 'react-router-dom'

function LoginRegisterToggle() {
  return (
    <div className='W-full flex justify-around mb-8 p-1 bg-white/30 rounded-l-3xl rounded-r-3xl'>
        <NavLink to="/login" className={ ({ isActive }) => isActive ? "text-primary text-xl bg-green-400 h-full flex relative rounded-l-3xl rounded-r-3xl pl-6 pr-6 pt-1 pb-1" : "text-white text-xl h-full flex relative rounded-l-3xl rounded-r-3xl pl-4 pr-4 pt-1 pb-1" }>
            Login
        </NavLink>
        <NavLink to="/register" className={ ({ isActive }) => isActive ? "text-primary text-xl bg-green-400 h-full flex relative rounded-l-3xl rounded-r-3xl pl-6 pr-6 pt-1 pb-1" : "text-white text-xl h-full flex relative rounded-l-3xl rounded-r-3xl pl-4 pr-4 pt-1 pb-1" }>
            Register
        </NavLink>
    </div>
  )
}

export default LoginRegisterToggle