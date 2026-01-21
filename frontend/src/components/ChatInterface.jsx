import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, RefreshCcw, Sparkles, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { API } from '../lib/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Neural interface initialized. I am ready to assist you with enterprise tasks.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useContext, setUseContext] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const data = await API.chat(userMsg, useContext);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response,
        meta: { 
          time: data.processing_time,
          contextUsed: data.context_used
        }
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: Unable to reach neural core." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full relative overflow-hidden">
      {/* Header / Controls */}
      <div className="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-black/20 backdrop-blur-sm z-10">
        <div className="flex items-center gap-2">
           <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
           <span className="text-sm font-mono text-zinc-400">LIVE SESSION</span>
        </div>
        
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setUseContext(!useContext)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              useContext 
                ? 'bg-jarvis-accent/10 text-jarvis-accent border border-jarvis-accent/20' 
                : 'bg-zinc-800 text-zinc-400 border border-zinc-700'
            }`}
          >
            <Database size={12} />
            RAG {useContext ? 'ON' : 'OFF'}
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <AnimatePresence>
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center shrink-0 border border-white/5">
                  <Bot size={16} className="text-jarvis-accent" />
                </div>
              )}
              
              <div className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                msg.role === 'user' 
                  ? 'bg-white text-black rounded-tr-sm' 
                  : 'bg-zinc-900 border border-white/10 rounded-tl-sm text-zinc-200'
              }`}>
                <p className="leading-relaxed text-sm whitespace-pre-wrap">{msg.content}</p>
                {msg.meta && (
                  <div className="mt-2 pt-2 border-t border-white/5 flex items-center gap-3 text-[10px] text-zinc-500 font-mono">
                    <span>{msg.meta.time.toFixed(3)}s latency</span>
                    {msg.meta.contextUsed && (
                      <span className="flex items-center gap-1 text-jarvis-accent/70">
                        <Database size={8} /> Context Retrieved
                      </span>
                    )}
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center shrink-0 border border-white/5">
                  <User size={16} className="text-zinc-400" />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isLoading && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-4"
          >
            <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center shrink-0 border border-white/5">
              <Bot size={16} className="text-jarvis-accent" />
            </div>
            <div className="bg-zinc-900 border border-white/10 rounded-2xl rounded-tl-sm px-5 py-4 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-jarvis-accent/50 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 bg-jarvis-accent/50 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-jarvis-accent/50 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 pt-2">
        <div className="relative glass-panel rounded-xl p-2 flex items-end gap-2 focus-within:ring-1 focus-within:ring-jarvis-accent/50 transition-all">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
            placeholder="Enter command or query..."
            className="w-full bg-transparent border-none text-sm text-white placeholder-zinc-500 focus:ring-0 resize-none max-h-32 p-3 font-mono"
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="p-3 rounded-lg bg-white text-black hover:bg-zinc-200 disabled:opacity-50 disabled:hover:bg-white transition-colors"
          >
            {isLoading ? <RefreshCcw size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
        </div>
        <div className="text-center mt-2">
           <span className="text-[10px] text-zinc-600 font-mono">ENCRYPTED // LOCALHOST // MODEL:LLAMA-2</span>
        </div>
      </div>
    </div>
  );
}
