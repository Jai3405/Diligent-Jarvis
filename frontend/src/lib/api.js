export const API = {
  async healthCheck() {
    try {
      const res = await fetch('/health');
      return await res.json();
    } catch (e) {
      return { status: 'offline' };
    }
  },

  async chat(message, useContext = true) {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, use_context: useContext })
    });
    return await res.json();
  },

  async addKnowledge(text, source) {
    const res = await fetch('/knowledge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        text, 
        metadata: { source } 
      })
    });
    return await res.json();
  }
};
