import React, { useEffect, useState } from 'react'
import authAxios from '../api/apiConfig';

const AddContact = ( { setaddContactPage } ) => {

    const [contacts, setContacts] = useState(null);

    useEffect(() => {
        async function fetch_contacts() {
            const res = await authAxios.get("/my-contacts");
            setContacts(res.data);
            console.log(res.data);
        }
        fetch_contacts();
    }, [])
  return (
    <div className='bg-secondary w-1/3 h-1/3 rounded-lg p-6 flex flex-col'>
        <div className='text-2xl mb-4'>Add Contact</div>
        <input type="text" placeholder='Enter username' className='rounded-md text-2xl p-2 bg-white/70 text-black focus:bg-white/5 focus:text-white outline-none mb-4'/>

            <div className='flex justify-end gap-4'>
                    <button className='bg-white/30 text-white px-4 py-2 rounded-md hover:bg-white/50' onClick={() => setaddContactPage(false)}>Cancel</button>
                    <button className='bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700'>🔍</button>
            </div>
            {contacts && (
                <div className='mt-4 flex-1 overflow-y-auto'>
                    <span className='text-lg mb-2'>Your Contacts</span>
                </div>
            )}
            {contacts.map((contact) => (
                    <div key={contact.id} className='p-2 mb-2 bg-white/10 rounded-md flex justify-between items-center cursor-pointer hover:bg-white/20'>
                        <div className='flex items-center gap-4 '>
                            <img src={contact.profile_pic || "/Profile Photos/blank_profile.png"} alt="" className='h-10 w-10 rounded-full'/>
                            <span className='text-lg text-white'>@{contact.username}</span>
                        </div>
                        <div className='flex gap-4'>
                            <button className='bg-green-600 text-white px-4 py-2 hover:bg-green-700 rounded-full'>+</button>
                            <button className='bg-blue-600 text-white px-4 hover:bg-blue-700 rounded-md'>Chat</button>
                        </div>
                    </div>
            ))}
    </div>
  )
}

export default AddContact