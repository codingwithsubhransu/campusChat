import React, { use, useEffect, useRef, useState } from 'react';
import authAxios from '../api/apiConfig';

const ChatHistory = ({ id, activeWindow, message, setMessage }) => {
    const socketRef = useRef(null);
    const [chatHistory, setChatHistory] = useState([]);

    // 1. Initialize WebSocket once when the component mounts
    useEffect(() => {
       // Use window.location.hostname to ensure the origin always matches
        const host = window.location.hostname === 'localhost' ? '127.0.0.1' : window.location.hostname;
        socketRef.current = new WebSocket(`ws://${host}:8000/api/ws/chat?token=${localStorage.getItem('access_token')}`);

        socketRef.current.onopen = () => console.log("Connected to chat server");

        socketRef.current.onmessage = (event) => {
            const newMessage = JSON.parse(event.data);
            // Append new message to local state
            setChatHistory((prev) => [...prev, newMessage]);
        };

        socketRef.current.onclose = () => console.log("Disconnected");

        // Cleanup on unmount
        return () => {
            if (socketRef.current) socketRef.current.close();
        };
    }, []); // Empty dependency array means this runs ONCE

    

    // 2. Function to send message
    const sendMessage = (e) => {
        if (e.key === 'Enter' && message.trim() !== "") {
            const payload = {
                receiver_id: activeWindow.id, // Ensure this matches your backend expectation
                group_id: null,
                content: message
            };
            socketRef.current.send(JSON.stringify(payload));
            setMessage(""); // Clear input
        }
    };


    useEffect(() => {
      async function fetch_chat_history() {
        const res = await authAxios.get('/history/' + id);
        setChatHistory(res.data);
        console.log(res.data);
      }
        fetch_chat_history();
        console.log("Fetching chat history for ID:", id);
    }, [id])
    

    return (
        <div className='h-full flex flex-col'>
            {/* Header */}
            <div className='chat-header h-20 border-b-2 border-white/30 flex items-center justify-between p-4'>
                <div className='flex items-center'>
                    <img src={activeWindow.profile_pic || "/Profile Photos/blank_profile.png"} alt="" className='h-10 w-10 rounded-full'/>
                    <span className='text-xl text-white ml-4'>{activeWindow.username}</span>
                </div>
                <div className='flex items-center gap-3 text-white'>
                    <span>&#8942;</span>
                    <span className='bg-white h-8 w-8 rounded-full text-xl text-black flex justify-center items-center'>i</span>
                </div>
            </div>

            {/* Messages Area */}
            <div className='chat-messages flex-1 p-4 text-white flex flex-col overflow-y-auto'>
                {chatHistory.map((msg, index) => (
                    <div key={index} 
                         className={`mb-4 ${msg.sender_id === id ? 'self-start' : 'self-end'} flex flex-col`}>
                        <p className={`rounded-lg p-3 max-w-md ${msg.sender_id === id ? 'bg-white/25' : ' bg-green-600'}`}>
                            {msg.content}
                        </p>
                        <span className='text-[10px] text-white/50 mt-1'>
                            {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    </div>
                ))}
            </div>

            {/* Input Area */}
            <div className='chat-input h-20 border-t-2 border-white/30 flex items-center p-4 gap-5'>
                <input 
                    type="text" 
                    placeholder='Type a message...' 
                    className='w-full rounded-md p-4 bg-white/20 text-white text-xl outline-none focus:bg-white/10' 
                    value={message} 
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={sendMessage} // Trigger on Enter key
                />
                <button onClick={sendMessage} className='bg-green-500 py-4 px-6 text-xl rounded-lg'>Send</button>
            </div>
        </div>
    );
}

export default ChatHistory;