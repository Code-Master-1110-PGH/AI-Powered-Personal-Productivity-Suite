'use client';

import React, { useState, useEffect } from 'react';
import { Sparkles, Brain, Clock, Zap, CheckCircle2, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface HeaderProps {
  activeTab: 'all' | 'scheduler' | 'resume';
  setActiveTab: (tab: 'all' | 'scheduler' | 'resume') => void;
  userId: number;
  setUserId: (id: number) => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  userId,
  setUserId,
}) => {
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/health');
        setBackendHealthy(res.ok);
      } catch {
        setBackendHealthy(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-border-subtle backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo & Title */}
        <div className="flex items-center space-x-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center shadow-glow-cyan">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <motion.div
              className="absolute -top-1 -right-1 w-3 h-3 bg-neon-cyan rounded-full"
              animate={{ scale: [1, 1.4, 1], opacity: [0.8, 1, 0.8] }}
              transition={{ repeat: Infinity, duration: 2 }}
            />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-cyan-200 to-purple-300">
                SYNAPSE OS
              </h1>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-950/60 text-neon-cyan border border-cyan-500/30 font-mono font-medium">
                v1.0 ENTERPRISE
              </span>
            </div>
            <p className="text-xs text-slate-400">AI Personal Productivity & Career Suite</p>
          </div>
        </div>

        {/* View Mode Switcher */}
        <nav className="hidden md:flex items-center p-1 rounded-xl bg-slate-900/80 border border-slate-800">
          <button
            onClick={() => setActiveTab('all')}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'all'
                ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-white border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-neon-cyan" />
            <span>Dual Command Center</span>
          </button>

          <button
            onClick={() => setActiveTab('scheduler')}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'scheduler'
                ? 'bg-cyan-500/20 text-white border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>Smart Scheduler</span>
          </button>

          <button
            onClick={() => setActiveTab('resume')}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'resume'
                ? 'bg-purple-500/20 text-white border border-purple-500/40 shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Brain className="w-3.5 h-3.5 text-purple-400" />
            <span>Resume Vault</span>
          </button>
        </nav>

        {/* User Context & Backend Live Health Indicator */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-xs text-slate-300 bg-slate-900/60 px-3 py-1.5 rounded-lg border border-slate-800">
            <span className="text-slate-500">User ID:</span>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-12 bg-slate-950 text-white border border-slate-700 rounded px-1.5 py-0.5 text-center text-xs font-mono focus:border-cyan-400 focus:outline-none"
              min="1"
            />
          </div>

          <div className="flex items-center space-x-1.5 text-xs px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800">
            {backendHealthy === true ? (
              <>
                <span className="w-2 h-2 rounded-full bg-neon-emerald animate-pulse" />
                <span className="text-emerald-400 font-mono text-[11px]">API 8000 LIVE</span>
              </>
            ) : backendHealthy === false ? (
              <>
                <span className="w-2 h-2 rounded-full bg-red-500" />
                <span className="text-red-400 font-mono text-[11px]">OFFLINE</span>
              </>
            ) : (
              <span className="text-slate-500 text-[11px]">CONNECTING...</span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

