import { useState } from 'react'
import Login from './Components/Authentication/Login'
import Register from './Components/Authentication/Register'
import { Routes, Route } from 'react-router-dom'
import ChatsScreen from './Components/Chats/ChatsScreen'
import EmailVerification from './Components/Authentication/EmailVerification'
import ProtectedRoute from './Components/ProtectedRoute'


function App() {

  return (
    <>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/chats" element={<ChatsScreen />} />
        </Route>
        <Route path='/verify-email' element={<EmailVerification />} />
      </Routes>
    </>
  )
}

export default App
