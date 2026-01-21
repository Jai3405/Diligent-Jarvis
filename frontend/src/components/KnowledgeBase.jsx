import React, { useState } from 'react';
import { Save, FileText, Database, CheckCircle, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { API } from '../lib/api';

export default function KnowledgeBase() {
  const [text, setText] = useState('');
  const [source, setSource] = useState('');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error

  const handleIngest = async () => {
    if (!text.trim() || !source.trim()) return;
    
    setStatus('loading');
    try {
      await API.addKnowledge(text, source);
      setStatus('success');
      setTimeout(() => {
        setText('');
        setSource('');
        setStatus('idle');
      }, 2000);
    } catch (e) {
      setStatus('error');
    }
  };

  return (
    <div className="flex flex-col h-full p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-light mb-2">Memory Bank Ingestion</h2>
        <p className="text-zinc-500 text-sm">Add unstructured text data to the vector database for RAG retrieval.</p>
      </div>

      <div className="glass-panel p-6 rounded-xl space-y-6">
        <div className="space-y-2">
          <label className="text-xs font-mono text-zinc-400 uppercase tracking-wider">Source Identifier</label>
          <div className="relative group">
            <FileText className="absolute left-3 top-3 text-zinc-500 group-focus-within:text-jarvis-accent transition-colors" size={18} />
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              placeholder="e.g., Q3_Financial_Report.pdf"
              className="w-full bg-black/40 border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-sm text-white placeholder-zinc-600 focus:outline-none focus:border-jarvis-accent/50 transition-colors font-mono"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-mono text-zinc-400 uppercase tracking-wider">Content Payload</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste document content here..."
            className="w-full h-64 bg-black/40 border border-white/10 rounded-lg p-4 text-sm text-zinc-300 placeholder-zinc-600 focus:outline-none focus:border-jarvis-accent/50 transition-colors resize-none font-mono leading-relaxed"
          />
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-white/5">
          <div className="text-xs text-zinc-500">
            {text.length > 0 && <span>{text.length} characters ready for embedding</span>}
          </div>

          <button
            onClick={handleIngest}
            disabled={status === 'loading' || !text || !source}
            className={`flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
              status === 'success' 
                ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                : status === 'error'
                ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                : 'bg-white text-black hover:bg-zinc-200 disabled:opacity-50 disabled:hover:bg-white'
            }`}
          >
            {status === 'loading' && <Database className="animate-pulse" size={18} />}
            {status === 'success' && <CheckCircle size={18} />}
            {status === 'error' && <AlertCircle size={18} />}
            {status === 'idle' && <Save size={18} />}
            
            <span>
              {status === 'loading' ? 'Processing Vectors...' : 
               status === 'success' ? 'Ingestion Complete' : 
               status === 'error' ? 'Ingestion Failed' : 'Process & Embed'}
            </span>
          </button>
        </div>
      </div>

      {/* Visual Decorator */}
      <div className="mt-12 grid grid-cols-3 gap-4 opacity-30">
        {[1,2,3].map(i => (
          <div key={i} className="h-1 bg-gradient-to-r from-transparent via-jarvis-accent to-transparent rounded-full" />
        ))}
      </div>
    </div>
  );
}
