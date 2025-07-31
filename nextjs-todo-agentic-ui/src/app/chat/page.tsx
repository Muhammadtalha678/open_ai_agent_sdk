'use client';
import Image from "next/image";
import { useState } from "react";

export default function Chat() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Welcome! How can I help you with your todos?' }
    ]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        const userMessage = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);

        // const res = await fetch('http://localhost:8000/chat', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ message: input }),
        // });
        // const data = await res.json();
        const assistantMessage = { role: 'assistant', content: "How are you" };

        setMessages((prev) => [...prev, assistantMessage]);
        setInput('');
    };

    return (
        <div className="p-6 max-w-xl mx-auto">
            <div className="space-y-4 mb-4">
                {messages.map((msg, i) => (
                    <div key={i} className={`p-2 rounded ${msg.role === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-200'}`}>
                        {msg.content}
                    </div>
                ))}
            </div>
            <div className="flex gap-2">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-grow p-2 border rounded"
                    placeholder="Type your message..."
                />
                <button onClick={sendMessage} className="bg-blue-500 text-white px-4 rounded">
                    Send
                </button>
            </div>
        </div>
    );
}

