import { useState } from 'react';
import LabPage from './pages/LabPage';
import { LayoutDashboard, Beaker, Zap } from 'lucide-react';

function App() {
  const [activePage, setActivePage] = useState<'dashboard' | 'lab'>('lab');

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100">

      {/* 📟 Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-6 flex flex-col gap-8">
        <div className="flex items-center gap-3 px-2">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Zap size={20} className="fill-current" />
          </div>
          <span className="font-bold text-xl tracking-tight">TENNIS.AI</span>
        </div>

        <nav className="flex flex-col gap-2">
          <button 
            onClick={() => setActivePage('dashboard')}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activePage === 'dashboard' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            <LayoutDashboard size={18} />
            <span className="font-medium">Live Dashboard</span>
          </button>

          <button 
            onClick={() => setActivePage('lab')}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activePage === 'lab' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            <Beaker size={18} />
            <span className="font-medium">Model Lab</span>
          </button>
        </nav>

        <div className="mt-auto p-4 bg-slate-800/50 rounded-xl border border-slate-700/50">
          <p className="text-xs text-slate-500 uppercase font-bold tracking-widest">Model Version</p>
          <p className="text-sm font-mono text-blue-400 mt-1">v4.2.1-stable</p>
        </div>
      </aside>

      {/* 🚀 Main Content Area */}
      <main className="flex-1 overflow-y-auto">
        {activePage === 'lab' ? (
          <LabPage />
        ) : (
          <div className="p-8 flex items-center justify-center h-full text-slate-500">
            <p className="text-lg">Live Dashboard coming soon...</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
