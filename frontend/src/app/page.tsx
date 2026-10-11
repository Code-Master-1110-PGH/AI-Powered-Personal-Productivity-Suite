'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from '@/components/layout/Header';
import { SmartScheduler } from '@/components/micro/SmartScheduler';
import { ResumeReviewer } from '@/components/macro/ResumeReviewer';
import { MacroOverview } from '@/components/macro/MacroOverview';
import { ResumeAnalysis } from '@/types';
import { pageTransitionVariants } from '@/lib/animations';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'all' | 'scheduler' | 'resume'>('all');
  const [userId, setUserId] = useState<number>(1);
  const [currentAnalysis, setCurrentAnalysis] = useState<ResumeAnalysis | null>(null);
  const [scheduleCount, setScheduleCount] = useState<number>(3);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        userId={userId}
        setUserId={setUserId}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Macro KPI Stat Cards */}
        <MacroOverview
          analysis={currentAnalysis}
          scheduleCount={scheduleCount}
        />

        {/* Dynamic Dual-Pane vs Focused Layout with Framer Motion */}
        <AnimatePresence mode="wait">
          {activeTab === 'all' && (
            <motion.div
              key="dual-pane"
              variants={pageTransitionVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start"
            >
              {/* Left Pane: Micro-Productivity (Daily Smart Scheduler) */}
              <div className="lg:col-span-6 space-y-6">
                <div className="glass-panel-elevated rounded-3xl p-6 sm:p-7 border border-slate-800 shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-32 h-1 bg-gradient-to-r from-neon-cyan to-transparent" />
                  <SmartScheduler userId={userId} />
                </div>
              </div>

              {/* Right Pane: Macro-Productivity (Career Resume Vault) */}
              <div className="lg:col-span-6 space-y-6">
                <div className="glass-panel-elevated rounded-3xl p-6 sm:p-7 border border-slate-800 shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-1 bg-gradient-to-l from-neon-purple to-transparent" />
                  <ResumeReviewer
                    userId={userId}
                    onAnalysisComplete={(analysis) => setCurrentAnalysis(analysis)}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'scheduler' && (
            <motion.div
              key="scheduler-only"
              variants={pageTransitionVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="max-w-4xl mx-auto"
            >
              <div className="glass-panel-elevated rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-2xl">
                <SmartScheduler userId={userId} />
              </div>
            </motion.div>
          )}

          {activeTab === 'resume' && (
            <motion.div
              key="resume-only"
              variants={pageTransitionVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="max-w-4xl mx-auto"
            >
              <div className="glass-panel-elevated rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-2xl">
                <ResumeReviewer
                  userId={userId}
                  onAnalysisComplete={(analysis) => setCurrentAnalysis(analysis)}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="border-t border-border-subtle py-6 text-center text-xs text-slate-500">
        <p>
          Synapse OS • AI-Powered Personal Productivity Suite • FastAPI Backend & Next.js Motion
          Frontend
        </p>
      </footer>
    </div>
  );
}

