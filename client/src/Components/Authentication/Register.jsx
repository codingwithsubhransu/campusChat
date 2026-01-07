import React from 'react'
import LeftBackground from './LeftBackground'
import { useForm, Controller } from 'react-hook-form'
import LoginRegisterToggle from './LoginRegisterToggle'
import { Link } from 'react-router-dom'

const Login = () => {

    const {
        register,
        handleSubmit,
        control,
        formState: { errors }
    } = useForm();



    const HandleRegister = (data) => {
        console.log(data);
    }

  return (
    <div className='text-white text-3xl bg-primary w-screen h-screen flex md:flex-col lg:flex-row relative overflow-hidden'>
        <LeftBackground />
        <form className='w-1/2 h-full flex flex-col justify-start items-center mt-4 gap-9 p-4' onSubmit={handleSubmit(HandleRegister)}>
          <LoginRegisterToggle />
          <div className='w-full h-full flex flex-col gap-6 pl-16'>
            <h1 className='text-3xl'>Welcome</h1>
            <p className='text-lg opacity-40'>Please enter your details to register.</p>

            <label className='w-full flex flex-col gap-3 '>
              <h1 className='text-sm opacity-80'>Unique Username</h1>
              <Controller
                name="username"
                control={control}
                rules={{ required: true }}
                render={({ field }) => <input type="text" {...field} onChange={(e) => field.onChange(e.target.value.toLowerCase())} placeholder='johndoe' className='p-3 text-lg bg-white/10 rounded-2xl' />}
              />
              {errors.username && <span className='text-xl text-red-600'>This field is required</span>}
            </label>

            <label className='w-full flex flex-col gap-3 '>
              <h1 className='text-sm opacity-80'>Email</h1>
              <input type="text"  {...register("email", { required: true })} placeholder='student@university.in' className='p-3 text-lg bg-white/10 rounded-2xl'/>
              {errors.email && <span className='text-xl text-red-600'>This field is required</span>}
            </label>
            
            <label className='w-full flex flex-col gap-3 '>
              <h1 className='text-sm opacity-80'>Password</h1>
              <input type="password"  {...register("password", { required: true, pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/ })} className='p-3 text-lg bg-white/10 rounded-2xl' placeholder='............'/>
              {errors.password && <span className='text-xl text-red-600'>This field is required</span>}
            </label>

            <button type='submit' className='w-full bg-green-500 p-3 text-white text-xl rounded-2xl mt-4 hover:bg-green-600 transition duration-300'>Register</button>
          </div>
        </form>
    </div>
  )
}

export default Login