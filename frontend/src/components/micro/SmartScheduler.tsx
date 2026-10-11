'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Calendar,
  Clock,
  Sparkles,
  Send,
  CheckCircle,
  Circle,
  AlertTriangle,
  Flame,
  CheckCheck,
  ChevronRight,
  Filter,
  RefreshCw,
  Plus,
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { api } from '@/lib/api';
import { DailySchedule, Task, TaskPriority } from '@/types';
import {
  chatInputBarVariants,
  staggerContainerVariants,
  taskCardVariants,
} from '@/lib/animations';

interface SmartSchedulerProps {
  userId: number;
}

const SUGGESTIONS = [
  'Schedule a mock interview tomorrow at 5 PM for 90 mins',
  'Urgent system architecture review today at 3 PM',
  'Prepare slide deck next Monday at 10 AM for 45 mins',
  'Low priority team retrospective today at 6 PM',
];

export const SmartScheduler: React.FC<SmartSchedulerProps> = ({ userId }) => {
  const [prompt, setPrompt] = useState<string>('');
  const [isInputFocused, setIsInputFocused] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [schedules, setSchedules] = useState<DailySchedule[]>([]);
  const [filter, setFilter] = useState<'ALL' | 'URGENT' | 'COMPLETED'>('ALL');
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [error, setError] = useState<string | null>(null);
  const [lastExtractedMetadata, setLastExtractedMetadata] = useState<any | null>(null);

  // Fetch Itinerary on load and on date change
  const fetchItinerary = async () => {
    try {
      setError(null);
      const res = await api.getDailyItinerary(userId, selectedDate);
      setSchedules(res.itinerary || []);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to retrieve daily schedule.');
    }
  };

  useEffect(() => {
    fetchItinerary();
  }, [userId, selectedDate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isSubmitting) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await api.createSmartTask(userId, prompt);
      setPrompt('');
      setLastExtractedMetadata(response.nlu_metadata);

      // Trigger micro celebration
      confetti({
        particleCount: 40,
        spread: 60,
        origin: { y: 0.8 },
        colors: ['#00F0FF', '#A855F7', '#10B981'],
      });

      // Refresh schedule
      await fetchItinerary();
    } catch (err: any) {
      setError(err.message || 'Could not process scheduling instruction.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleTaskCompletion = (scheduleId: number) => {
    setSchedules((prev) =>
      prev.map((s) => {
        if (s.id === scheduleId) {
          const nextCompleted = !s.is_completed;
          if (nextCompleted) {
            confetti({
              particleCount: 25,
              spread: 45,
              origin: { y: 0.6 },
              colors: ['#10B981', '#38BDF8'],
            });
          }
          return { ...s, is_completed: nextCompleted };
        }
        return s;
      })
    );
  };

  const getPriorityBadge = (priority?: TaskPriority) => {
    switch (priority) {
      case 'URGENT':
        return {
          icon: <Flame className="w-3.5 h-3.5 text-neon-pink" />,
          label: 'URGENT',
          style: 'bg-red-500/20 text-red-300 border-red-500/40',
        };
      case 'HIGH':
        return {
          icon: <AlertTriangle className="w-3.5 h-3.5 text-neon-amber" />,
          label: 'HIGH',
          style: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
        };
      case 'LOW':
        return {
          icon: <Clock className="w-3.5 h-3.5 text-slate-400" />,
          label: 'LOW',
          style: 'bg-slate-800 text-slate-400 border-slate-700',
        };
      default:
        return {
          icon: <Sparkles className="w-3.5 h-3.5 text-neon-cyan" />,
          label: 'MEDIUM',
          style: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
        };
    }
  };

  const filteredSchedules = schedules.filter((item) => {
    if (filter === 'URGENT') {
      return item.task?.priority === 'URGENT' || item.task?.priority === 'HIGH';
    }
    if (filter === 'COMPLETED') {
      return item.is_completed;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Title & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-1.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              <Clock className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-white tracking-tight">Micro-Productivity Agenda</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Natural Language Task Extraction & Temporal Chronology Timeline
          </p>
        </div>

        {/* Date Selector & Refresh */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-slate-900/80 border border-slate-800 rounded-lg px-2.5 py-1 text-xs">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="bg-transparent text-slate-200 text-xs font-mono focus:outline-none cursor-pointer"
            />
          </div>

          <button
            onClick={fetchItinerary}
            className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-all"
            title="Refresh schedule"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Dynamic Glowing Chat-Input Bar */}
      <div className="space-y-2">
        <motion.form
          onSubmit={handleSubmit}
          variants={chatInputBarVariants}
          animate={isInputFocused ? 'focused' : 'idle'}
          className="relative rounded-2xl glass-panel p-2 flex items-center gap-2 border border-slate-800 transition-all"
        >
          <div className="pl-3 flex items-center text-neon-cyan">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>

          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onFocus={() => setIsInputFocused(true)}
            onBlur={() => setIsInputFocused(false)}
            placeholder="Type in plain English: 'Schedule a mock interview tomorrow at 5 PM'..."
            className="flex-1 bg-transparent border-none text-sm text-white placeholder-slate-500 focus:outline-none px-2 font-medium"
          />

          <button
            type="submit"
            disabled={!prompt.trim() || isSubmitting}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:opacity-40 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-glow-cyan transition-all"
          >
            {isSubmitting ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>Schedule</span>
                <Send className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </motion.form>

        {/* Quick Suggestion Chips */}
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <span className="text-[11px] text-slate-500 font-mono flex items-center space-x-1 mr-1">
            <span>Suggestions:</span>
          </span>
          {SUGGESTIONS.map((sug, idx) => (
            <button
              key={idx}
              onClick={() => setPrompt(sug)}
              className="text-[11px] font-mono px-2.5 py-1 rounded-md bg-slate-900/70 hover:bg-slate-800 text-slate-400 hover:text-cyan-300 border border-slate-800/80 transition-all truncate max-w-[280px]"
            >
              "{sug}"
            </button>
          ))}
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-red-950/40 border border-red-500/30 text-xs text-red-300 flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Real-time Extracted NLU Feedback Tag */}
        {lastExtractedMetadata && (
          <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/30 text-xs text-cyan-200 flex items-center justify-between"
          >
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-neon-cyan animate-pulse" />
              <span>
                Parsed Intent:{' '}
                <strong className="text-white">{lastExtractedMetadata.intent}</strong> • Title:{' '}
                <strong className="text-white">"{lastExtractedMetadata.extracted_title}"</strong>
              </span>
            </div>
            <span className="font-mono text-[10px] text-cyan-400">
              Confidence: {Math.round(lastExtractedMetadata.confidence_score * 100)}%
            </span>
          </motion.div>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between pt-2">
        <div className="flex items-center space-x-1.5 p-1 rounded-xl bg-slate-900/60 border border-slate-800">
          {(['ALL', 'URGENT', 'COMPLETED'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                filter === tab
                  ? 'bg-slate-800 text-white border border-slate-700 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab === 'ALL' ? 'All Blocks' : tab === 'URGENT' ? 'Urgent / High' : 'Completed'}
            </button>
          ))}
        </div>

        <span className="text-xs font-mono text-slate-500">
          {filteredSchedules.length} Event{filteredSchedules.length !== 1 ? 's' : ''} on{' '}
          {selectedDate}
        </span>
      </div>

      {/* Timeline View */}
      <div className="space-y-3 relative">
        <AnimatePresence mode="popLayout">
          {filteredSchedules.length > 0 ? (
            <motion.div
              variants={staggerContainerVariants}
              initial="hidden"
              animate="visible"
              className="space-y-3"
            >
              {filteredSchedules.map((schedule) => {
                const priorityBadge = getPriorityBadge(schedule.task?.priority);
                const startTime = new Date(schedule.start_time).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                });
                const endTime = new Date(schedule.end_time).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                });

                return (
                  <motion.div
                    key={schedule.id}
                    variants={taskCardVariants}
                    layout
                    className={`glass-panel rounded-2xl p-4.5 border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                      schedule.is_completed
                        ? 'opacity-60 border-slate-800 bg-slate-950/40'
                        : 'border-slate-800/90 hover:border-cyan-500/40 hover:shadow-glow-cyan'
                    }`}
                  >
                    <div className="flex items-start space-x-3.5">
                      <button
                        onClick={() => toggleTaskCompletion(schedule.id)}
                        className="mt-0.5 text-slate-500 hover:text-neon-emerald transition-colors"
                      >
                        {schedule.is_completed ? (
                          <CheckCircle className="w-5 h-5 text-neon-emerald" />
                        ) : (
                          <Circle className="w-5 h-5" />
                        )}
                      </button>

                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <h4
                            className={`text-sm font-bold text-white transition-all ${
                              schedule.is_completed ? 'line-through text-slate-500' : ''
                            }`}
                          >
                            {schedule.time_block_title}
                          </h4>
                          <span
                            className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold border ${priorityBadge.style}`}
                          >
                            {priorityBadge.icon}
                            <span>{priorityBadge.label}</span>
                          </span>
                        </div>

                        {schedule.task?.raw_prompt && (
                          <p className="text-xs text-slate-400 font-mono">
                            Prompt: "{schedule.task.raw_prompt}"
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center space-x-4 self-end sm:self-center">
                      <div className="text-right">
                        <span className="text-xs font-mono text-cyan-300 font-semibold block">
                          {startTime} – {endTime}
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {schedule.task?.estimated_duration_minutes || 60} min block
                        </span>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass-panel rounded-2xl p-10 text-center space-y-3 border border-slate-800"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-900 border border-slate-800 mx-auto flex items-center justify-center text-slate-500">
                <Calendar className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-semibold text-slate-300">No events scheduled for this date</h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Use the AI command bar above to schedule a task in natural language, or pick another date.
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

