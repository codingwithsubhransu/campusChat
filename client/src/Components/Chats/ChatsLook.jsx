import React from 'react'

function ChatsLook({ id, profile_pic, username, last_message, timestamp, activeWindow}) {
  return (
    <div className={`w-full min-h-18 rounded-2xl flex p-2 items-center hover:bg-green-500/20 cursor-pointer ${activeWindow === id ? 'bg-green-500/20' : ''}`}>
        <img src={profile_pic} alt="" className='h-10 w-10 rounded-full '/>
        <div className='ml-4 flex-1'>
            <span className='text-xl text-white'>{username}</span>
            <p className='text-sm text-white/80'>{last_message}</p>
        </div>
        <span className='text-sm text-white/60'>{timestamp}</span>
    </div>
  )
}

export default ChatsLook