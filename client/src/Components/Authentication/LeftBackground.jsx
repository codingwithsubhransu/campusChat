import React from 'react'
import background from '/backgrounds/auth_background.png'

const LeftBackground = () => {
  return (
    <>
        <div className='w-1/2 h-full border-2 border-white inset-0 bg-cover bg-center opacity-70 mix-blend-overlay' style={{ backgroundImage: `url(${background})` }}>
        </div>
        <div className='absolute max-w-1/3 h-full flex flex-col justify-between pl-12'>
            <h1 className='pt-9'>CampusChat</h1>
            <div className='flex flex-col gap-7'>
                <h1 className=''>Private Campus<br /> <span className='text-green-400'>Connections</span></h1>
                <p className='text-sm'>Connect with fellow students and faculty in a secure and private environment designed exclusively for your campus community.</p>
                <div className='flex pb-28 -space-x-2'>
                    { ([1,2,3,4]).map((key, index) => (
                    <img src={`Profile Photos/Profile-${index+1}.png`} alt="" className='h-5 w-5 rounded-full border-white ring-2 ring-white' key={key}/>
                ))}
                <span className='text-sm pl-3 self-center'>99+ students are online. Join them</span>
                </div>
            </div>
        </div>
    </>
    
  )
}

export default LeftBackground