'use client';
import { apiCallPost } from "@/api/api_call";
import { AppRoutes } from "@/constant/AppRoutes";
import Image from "next/image";
import { FormEvent, useState } from "react";

export default function Chat() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Welcome! How can I help you with your todos?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        const userMessage = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);
        setLoading(true)
        const data = await apiCallPost(AppRoutes.chat, input)
        setLoading(false)
        console.log(data);
        const assistantMessage = { role: 'assistant', content: data };
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
            <form onSubmit={(e: FormEvent<HTMLFormElement>) => {
                e.preventDefault()
                sendMessage()
            }}>
                <div className="flex gap-2">

                    <input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        className="flex-grow p-2 border rounded"
                        placeholder="Type your message..."
                    />
                    <button type="submit" className="bg-blue-500 text-white px-4 rounded" disabled={loading}>
                        {loading ? (
                            <div className="flex justify-center">
                                <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                                    />
                                </svg>
                            </div>
                        ) : (
                            'Send'
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

