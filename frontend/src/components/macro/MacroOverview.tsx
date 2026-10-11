'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Award, Layers, TrendingUp, Clock } from 'lucide-react';
import { ResumeAnalysis, DailySchedule } from '@/types';

interface MacroOverviewProps {
  analysis: ResumeAnalysis | null;
  scheduleCount: number;
}

export const MacroOverview: React.FC<MacroOverviewProps> = ({
  analysis,
  scheduleCount,
}) => {
  const totalSkills = analysis
    ? analysis.skills.reduce((acc, cat) => acc + cat.skills.length, 0)
    : 0;

  const totalMetrics = analysis ? analysis.metrics.length : 0;
  const overallScore = analysis ? Math.round(analysis.overall_score) : '--';

  const stats = [
    {
      label: 'Career Readiness Index',
      value: overallScore,
      suffix: analysis ? '/ 100' : '',
      icon: <Award className="w-5 h-5 text-neon-cyan" />,
      color: 'from-cyan-500/20 to-blue-500/10',
      border: 'border-cyan-500/30',
      glow: 'shadow-glow-cyan',
    },
    {
      label: 'Core Competencies Indexed',
      value: totalSkills,
      suffix: 'Skills',
      icon: <Layers className="w-5 h-5 text-neon-purple" />,
      color: 'from-purple-500/20 to-pink-500/10',
      border: 'border-purple-500/30',
      glow: 'shadow-glow-purple',
    },
    {
      label: 'Quantified Impact Metrics',
      value: totalMetrics,
      suffix: 'KPIs',
      icon: <TrendingUp className="w-5 h-5 text-neon-emerald" />,
      color: 'from-emerald-500/20 to-teal-500/10',
      border: 'border-emerald-500/30',
      glow: 'shadow-glow-emerald',
    },
    {
      label: 'Active Agenda Slots',
      value: scheduleCount,
      suffix: 'Blocks',
      icon: <Clock className="w-5 h-5 text-blue-400" />,
      color: 'from-blue-500/20 to-indigo-500/10',
      border: 'border-blue-500/30',
      glow: '',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      {stats.map((stat, idx) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.08 }}
          whileHover={{ y: -3, transition: { duration: 0.2 } }}
          className={`glass-panel rounded-2xl p-4 border ${stat.border} bg-gradient-to-br ${stat.color} relative overflow-hidden transition-all`}
        >
          <div className="flex items-center justify-between">
            <span className="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
              {stat.icon}
            </span>
          </div>

          <div className="mt-3">
            <div className="flex items-baseline space-x-1.5">
              <span className="text-2xl font-black font-mono text-white tracking-tight">
                {stat.value}
              </span>
              <span className="text-xs text-slate-400 font-mono">{stat.suffix}</span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium mt-0.5 truncate">
              {stat.label}
            </p>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

