import React, { use, useEffect, useState } from 'react'
import ChatsLook from './ChatsLook'
import ChatHistory from './ChatHistory';
import AddContact from './AddContact';
import data from '../Data/DummyChat';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import authAxios from '../api/apiConfig';

const ChatsScreen = () => {

    const { user } = useAuth()

    const [activeWindow, setActiveWindow] = useState(null);
    const [message, setMessage] = useState("");
    const [contacts, setContacts] = useState(null);
    const [addContactPage, setaddContactPage]  = useState(false);

    useEffect(() => {
        async function fetch_contacts() {
            const res = await authAxios.get("/recent-chats");
            setContacts(res.data);
            console.log(res.data);
        }
        fetch_contacts();
    }, [])

  return (
    <div className='text-3xl text-white flex h-screen w-screen'>

        {addContactPage && (
            <div className='fixed top-0 left-0 w-screen h-screen bg-black/50 flex justify-center items-center z-50'>
                <AddContact setaddContactPage={setaddContactPage}/>
            </div>
        )}
        <div className='border-2 border-r-white/30 border-l-0 border-t-0 border-b-0 relative top-0 left-0 h-full w-1/4 flex flex-col bg-secondary'>
            <div className='current-user h-35 border-b-2 border-white/30 flex p-4 flex-col justify-between'>
            
                <div className='flex p-2 justify-between items-center'>
                    <div className='flex'>
                        <img src="/Profile Photos/Profile-1.png" alt="" className='h-8 w-8 rounded-full'/>
                    <span className='text-lg text-white ml-4'>@{user}</span>
                    </div>

                    <div className='flex justify-center items-center gap-4'>
                        <button className='bg-transparent text-3xl text-white/70 h-9 w-9 rounded-full cursor-pointer hover:bg-white/30' about='Add Contacts' onClick={() => setaddContactPage(true)}>+</button>
                        <div className='options text-2xl cursor-pointer text-white/70 hover:text-white'>
                            &#8942;
                        </div>
                    </div>
                </div>
                <input type="text" placeholder='Search by username' className='rounded-md text-lg p-2 bg-white/70 text-black focus:bg-white/5 focus:text-white outline-none'/>
            </div>
            <div className='chats-list p-2 flex flex-col gap-4 flex-1 overflow-y-auto w-full'>
                <span className='text-sm text-white/80'>Recent Chats</span>
                <div className='w-full h-full'>

                    {contacts && contacts.map((chat) => (
                        <div key={chat.id} onClick={() => setActiveWindow(chat)}>
                            <ChatsLook id={chat.id} profile_pic={chat.profile_pic || "/Profile Photos/blank_profile.png"} username={chat.username} last_message={chat.last_message} activeWindow={activeWindow ? activeWindow.id : null} timestamp={chat.timestamp} />
                        </div>
                    ))}
                </div>
            </div>
        </div>

        <div className='chat-window flex-1'>
            {activeWindow ? (
                <ChatHistory id={activeWindow.id} activeWindow={activeWindow} message={message} setMessage={setMessage}/>
            ) : (
                <div className='h-full flex items-center justify-center text-white/70'>
                    <span>Select a chat to start messaging</span>
                </div>
            )}
        </div>

    </div>
  )
}

export default ChatsScreen