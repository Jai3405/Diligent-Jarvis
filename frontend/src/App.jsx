import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import KnowledgeBase from './components/KnowledgeBase';
import { API } from './lib/api';

function App() {
  const [activeView, setActiveView] = useState('chat');
  const [systemStatus, setSystemStatus] = useState('checking');

  useEffect(() => {
    const checkHealth = async () => {
      const health = await API.healthCheck();
      setSystemStatus(health.status === 'healthy' ? 'online' : 'offline');
    };
    checkHealth();
    // Poll every 30s
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-black text-white selection:bg-jarvis-accent/30 selection:text-white">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-zinc-900 via-black to-black pointer-events-none" />
      <div className="scanline" />
      
      {/* Layout */}
      <div className="flex w-full h-full relative z-10 max-w-[1920px] mx-auto border-x border-white/5">
        <Sidebar 
          activeView={activeView} 
          setActiveView={setActiveView} 
          systemStatus={systemStatus}
        />
        
        <main className="flex-1 h-full relative">
          {activeView === 'chat' && <ChatInterface />}
          {activeView === 'knowledge' && <KnowledgeBase />}
        </main>
      </div>
    </div>
  );
}

export default App;
