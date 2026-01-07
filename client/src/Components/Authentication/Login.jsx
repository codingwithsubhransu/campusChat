import React from 'react'
import LeftBackground from './LeftBackground'
import { useForm } from 'react-hook-form'
import LoginRegisterToggle from './LoginRegisterToggle'
import { Link } from 'react-router-dom'
import authAxios from '../api/apiConfig'

const Login = () => {

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm();

    const handleLogin = async (data) => {
        const res = await authAxios.post('/login', data);
        localStorage.setItem('access_token', res.data.access_token);
        if (res.status === 200) {
            window.location.href = '/chats';
        } else {
            alert('Login failed. Please check your credentials.');
        }
    }



  return (
    <div className='text-white text-3xl bg-primary w-screen h-screen flex md:flex-col lg:flex-row relative overflow-hidden'>
        <LeftBackground />
        <form className='w-1/2 h-full flex flex-col justify-start items-center mt-4 gap-9 p-4' onSubmit={handleSubmit((data) => handleLogin(data))}>
          <LoginRegisterToggle />
          <div className='w-full h-full flex flex-col gap-6 pl-16'>
            <h1 className='text-3xl'>Welcome Back</h1>
            <p className='text-lg opacity-40'>Please enter your credentials to log in.</p>

            <label className='w-full flex flex-col gap-3 '>
              <h1 className='text-sm opacity-80'>Username or Email</h1>
              <input type="text"  {...register("username_or_email", { required: true })} placeholder='student@university.in' className='p-3 text-lg bg-white/10 rounded-2xl'/>
              {errors.username_or_email && <span>This field is required</span>}
            </label>
            
            <label className='w-full flex flex-col gap-3 '>
              <h1 className='text-sm opacity-80'>Password</h1>
              <input type="password"  {...register("password", { required: true })} className='p-3 text-lg bg-white/10 rounded-2xl' placeholder='............'/>
              {errors.password && <span>This field is required</span>}
            </label>
            <Link to="/forgot-password" className='text-sm text-white/70 hover:text-white w-full text-right'>Forgot Password?</Link>
            <button type='submit' className='w-full bg-green-500 p-3 text-white text-xl rounded-2xl mt-4 hover:bg-green-600 transition duration-300'>Login</button>
          </div>
        </form>
    </div>
  )
}

export default Login