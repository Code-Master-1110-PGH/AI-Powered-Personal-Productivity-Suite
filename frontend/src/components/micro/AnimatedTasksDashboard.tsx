'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  Circle,
  Clock,
  Flame,
  AlertTriangle,
  Sparkles,
  Calendar,
  Plus,
  Trash2,
} from 'lucide-react';
import confetti from 'canvas-confetti';

export type PriorityLevel = 'URGENT' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface TaskItem {
  id: string;
  title: string;
  timeSlot: string;
  priority: PriorityLevel;
  durationMinutes: number;
  isCompleted: boolean;
  category: string;
}

const INITIAL_TASKS: TaskItem[] = [
  {
    id: 't-1',
    title: 'High-Concurrency Distributed Systems Architecture Review',
    timeSlot: '09:00 - 10:30',
    priority: 'URGENT',
    durationMinutes: 90,
    isCompleted: false,
    category: 'System Design',
  },
  {
    id: 't-2',
    title: 'Mock Coding Interview (Graphs & Dynamic Programming)',
    timeSlot: '11:00 - 12:30',
    priority: 'HIGH',
    durationMinutes: 90,
    isCompleted: false,
    category: 'Interview Prep',
  },
  {
    id: 't-3',
    title: 'Profile Backend DB Query Latency with EXPLAIN ANALYZE',
    timeSlot: '14:00 - 15:00',
    priority: 'MEDIUM',
    durationMinutes: 60,
    isCompleted: false,
    category: 'Performance',
  },
  {
    id: 't-4',
    title: 'Refactor Repository Data Access Layer to Unit-of-Work',
    timeSlot: '16:00 - 17:00',
    priority: 'LOW',
    durationMinutes: 60,
    isCompleted: true,
    category: 'Refactoring',
  },
];

/**
 * Highly Animated Daily Tasks Dashboard Showcase Component.
 * Demonstrates Staggered Entrance Physics, Neon Glow Hover States,
 * and Liquid Slide-in/Slide-out Transitions.
 */
export const AnimatedTasksDashboard: React.FC = () => {
  const [tasks, setTasks] = useState<TaskItem[]>(INITIAL_TASKS);
  const [filter, setFilter] = useState<'ALL' | 'ACTIVE' | 'COMPLETED'>('ALL');
  const [newTitle, setNewTitle] = useState('');

  const toggleTask = (id: string) => {
    setTasks((prev) =>
      prev.map((t) => {
        if (t.id === id) {
          const nextState = !t.isCompleted;
          if (nextState) {
            confetti({
              particleCount: 35,
              spread: 50,
              origin: { y: 0.7 },
              colors: ['#00F0FF', '#10B981', '#A855F7'],
            });
          }
          return { ...t, isCompleted: nextState };
        }
        return t;
      })
    );
  };

  const removeTask = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const addTask = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    const newTask: TaskItem = {
      id: `t-${Date.now()}`,
      title: newTitle.trim(),
      timeSlot: '17:30 - 18:30',
      priority: 'HIGH',
      durationMinutes: 60,
      isCompleted: false,
      category: 'Focus Task',
    };

    setTasks((prev) => [newTask, ...prev]);
    setNewTitle('');

    confetti({
      particleCount: 25,
      spread: 45,
      origin: { y: 0.8 },
      colors: ['#38BDF8', '#8B5CF6'],
    });
  };

  const filteredTasks = tasks.filter((t) => {
    if (filter === 'ACTIVE') return !t.isCompleted;
    if (filter === 'COMPLETED') return t.isCompleted;
    return true;
  });

  const getPriorityStyle = (priority: PriorityLevel) => {
    switch (priority) {
      case 'URGENT':
        return {
          icon: <Flame className="w-3.5 h-3.5 text-neon-pink" />,
          badge: 'bg-red-500/20 text-red-300 border-red-500/40',
          glow: 'group-hover:border-red-500/50 group-hover:shadow-[0_0_20px_-3px_rgba(244,63,94,0.35)]',
        };
      case 'HIGH':
        return {
          icon: <AlertTriangle className="w-3.5 h-3.5 text-neon-amber" />,
          badge: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
          glow: 'group-hover:border-amber-500/50 group-hover:shadow-[0_0_20px_-3px_rgba(245,158,11,0.35)]',
        };
      case 'MEDIUM':
        return {
          icon: <Sparkles className="w-3.5 h-3.5 text-neon-cyan" />,
          badge: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
          glow: 'group-hover:border-cyan-500/50 group-hover:shadow-[0_0_25px_-3px_rgba(0,240,255,0.35)]',
        };
      case 'LOW':
        return {
          icon: <Clock className="w-3.5 h-3.5 text-slate-400" />,
          badge: 'bg-slate-800 text-slate-400 border-slate-700',
          glow: 'group-hover:border-slate-700 group-hover:shadow-[0_0_15px_-3px_rgba(148,163,184,0.2)]',
        };
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6 p-6 rounded-3xl glass-panel-elevated border border-slate-800 shadow-2xl relative overflow-hidden">
      {/* Top Ambient Cyber Flare */}
      <div className="absolute top-0 left-1/4 right-1/4 h-1 bg-gradient-to-r from-transparent via-neon-cyan to-transparent shadow-[0_0_25px_#00F0FF]" />

      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-neon-cyan animate-pulse" />
            <span>Interactive Daily Execution Grid</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Physics-based Framer Motion transitions & dynamic neon glow states
          </p>
        </div>

        {/* Tab Filters */}
        <div className="flex items-center space-x-1 p-1 rounded-xl bg-slate-900/80 border border-slate-800">
          {(['ALL', 'ACTIVE', 'COMPLETED'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                filter === tab
                  ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-white border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Add Form */}
      <form onSubmit={addTask} className="flex gap-2">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Add high-impact task with spring transition..."
          className="flex-1 bg-slate-950/70 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/40 transition-all font-medium"
        />
        <button
          type="submit"
          disabled={!newTitle.trim()}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 disabled:opacity-40 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-glow-cyan transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>Add Task</span>
        </button>
      </form>

      {/* Animated Task Cards Grid */}
      <motion.div
        layout
        className="space-y-3"
      >
        <AnimatePresence mode="popLayout">
          {filteredTasks.map((task, index) => {
            const pStyle = getPriorityStyle(task.priority);

            return (
              <motion.div
                key={task.id}
                layout
                initial={{ opacity: 0, y: -20, scale: 0.95 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  scale: 1,
                  transition: {
                    type: 'spring',
                    damping: 22,
                    stiffness: 280,
                    delay: index * 0.05,
                  },
                }}
                exit={{
                  opacity: 0,
                  x: -60,
                  scale: 0.9,
                  filter: 'blur(6px)',
                  transition: { duration: 0.25 },
                }}
                whileHover={{
                  y: -3,
                  scale: 1.01,
                  transition: { duration: 0.2, ease: 'easeOut' },
                }}
                onClick={() => toggleTask(task.id)}
                className={`group relative rounded-2xl p-4 border transition-all cursor-pointer backdrop-blur-xl ${
                  task.isCompleted
                    ? 'bg-slate-950/40 border-slate-800/80 opacity-60'
                    : `bg-slate-900/60 border-slate-800/90 ${pStyle.glow}`
                }`}
              >
                <div className="flex items-center justify-between gap-4">
                  {/* Left: Checkmark & Title */}
                  <div className="flex items-center space-x-3.5 flex-1 min-w-0">
                    <motion.div
                      whileTap={{ scale: 0.8 }}
                      className="text-slate-500 group-hover:text-neon-emerald transition-colors flex-shrink-0"
                    >
                      {task.isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-neon-emerald" />
                      ) : (
                        <Circle className="w-5 h-5" />
                      )}
                    </motion.div>

                    <div className="min-w-0 flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-[10px] font-mono text-slate-500 px-2 py-0.5 rounded bg-slate-800">
                          {task.category}
                        </span>
                        <span
                          className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold border ${pStyle.badge}`}
                        >
                          {pStyle.icon}
                          <span>{task.priority}</span>
                        </span>
                      </div>

                      <h4
                        className={`text-sm font-semibold text-white mt-1 truncate transition-all ${
                          task.isCompleted ? 'line-through text-slate-500' : ''
                        }`}
                      >
                        {task.title}
                      </h4>
                    </div>
                  </div>

                  {/* Right: Timestamp & Action */}
                  <div className="flex items-center space-x-3 flex-shrink-0">
                    <div className="text-right">
                      <span className="text-xs font-mono font-semibold text-cyan-300 block">
                        {task.timeSlot}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        {task.durationMinutes} mins
                      </span>
                    </div>

                    <button
                      onClick={(e) => removeTask(task.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-red-500/20 text-slate-500 hover:text-red-400 transition-all"
                      title="Delete Task"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

