import React from 'react';
import { Terminal, Database, Shield, Activity, Settings, Cpu } from 'lucide-react';

export default function Sidebar({ activeView, setActiveView, systemStatus }) {
  const navItems = [
    { id: 'chat', icon: Terminal, label: 'Neural Chat' },
    { id: 'knowledge', icon: Database, label: 'Memory Bank' },
  ];

  return (
    <div className="w-64 h-full glass-panel border-r border-white/10 flex flex-col justify-between p-4">
      <div>
        <div className="flex items-center gap-3 px-4 py-6 mb-6">
          <div className="w-10 h-10 rounded-full bg-jarvis-accent/10 border border-jarvis-accent/30 flex items-center justify-center">
            <Cpu className="w-6 h-6 text-jarvis-accent" />
          </div>
          <div>
            <h1 className="font-mono font-bold tracking-wider text-lg">JARVIS</h1>
            <p className="text-xs text-zinc-500 font-mono">v2.0.4 Enterprise</p>
          </div>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                activeView === item.id 
                  ? 'bg-white/10 text-white border border-white/5' 
                  : 'text-zinc-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <item.icon size={18} />
              <span className="font-medium text-sm">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="space-y-4">
        <div className="p-4 rounded-lg bg-black/40 border border-white/5 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-zinc-400">
            <span>SYSTEM STATUS</span>
            <Activity size={12} className={systemStatus === 'online' ? 'text-green-500' : 'text-red-500'} />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-zinc-500">LLM Engine</span>
              <span className="text-green-400">Ready</span>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-zinc-500">Vector DB</span>
              <span className="text-green-400">Connected</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2 px-2 text-xs text-zinc-600 font-mono">
          <Shield size={12} />
          <span>SECURE CONNECTION ESTABLISHED</span>
        </div>
      </div>
    </div>
  );
}
