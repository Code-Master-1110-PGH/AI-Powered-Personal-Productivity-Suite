'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  Upload,
  Sparkles,
  Award,
  CheckCircle2,
  TrendingUp,
  Cpu,
  Layers,
  ArrowRight,
  Database,
  Cloud,
  Code2,
  FileCheck,
  RotateCcw,
  Brain,
} from 'lucide-react';
import { api } from '@/lib/api';
import { ResumeAnalysis } from '@/types';
import {
  staggerContainerVariants,
  skillBadgeVariants,
  scanLaserVariants,
} from '@/lib/animations';

interface ResumeReviewerProps {
  userId: number;
  onAnalysisComplete?: (analysis: ResumeAnalysis) => void;
}

const SAMPLE_RESUME = `Alex Mercer
Senior Distributed Systems Architect & Backend Lead

Professional Summary:
Passionate Systems Architect with 8+ years experience designing ultra-low-latency distributed platforms, high-throughput microservices, and event-driven data pipelines.

Core Experience:
• Architected high-throughput microservices using Python, FastAPI, and PostgreSQL processing 50k QPS.
• Improved API response latency by 45% under 150ms for 10M+ daily active users on AWS.
• Led a team of 8 engineers and migrated legacy monolithic systems to Docker, Kubernetes, and Kafka.
• Reduced cloud infrastructure expenditures by $250K annually through automated elasticity.
• Mentored 5 junior developers and improved CI/CD build deployment reliability to 99.99% uptime.`;

export const ResumeReviewer: React.FC<ResumeReviewerProps> = ({
  userId,
  onAnalysisComplete,
}) => {
  const [resumeText, setResumeText] = useState<string>('');
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [scanProgress, setScanProgress] = useState<number>(0);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load existing analysis if user has one
  useEffect(() => {
    const loadRecent = async () => {
      try {
        const histories = await api.getUserResumes(userId);
        if (histories && histories.length > 0) {
          setAnalysis(histories[0]);
          if (onAnalysisComplete) onAnalysisComplete(histories[0]);
        }
      } catch {
        // User may not have resumes yet
      }
    };
    loadRecent();
  }, [userId]);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      readFile(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      readFile(e.target.files[0]);
    }
  };

  const readFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setResumeText(content);
    };
    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    if (!resumeText || resumeText.trim().length < 20) {
      setError('Please provide at least 20 characters of resume text or use the sample resume.');
      return;
    }

    setError(null);
    setIsScanning(true);
    setScanProgress(0);

    // Simulate scanning progress timeline for maximum visual impact
    const progressInterval = setInterval(() => {
      setScanProgress((prev) => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return 95;
        }
        return prev + 15;
      });
    }, 180);

    try {
      const result = await api.analyzeResume(userId, resumeText);
      clearInterval(progressInterval);
      setScanProgress(100);

      setTimeout(() => {
        setIsScanning(false);
        setAnalysis(result);
        if (onAnalysisComplete) onAnalysisComplete(result);
      }, 600);
    } catch (err: any) {
      clearInterval(progressInterval);
      setIsScanning(false);
      setError(err.message || 'Failed to analyze resume.');
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-neon-emerald';
    if (score >= 60) return 'text-neon-cyan';
    return 'text-neon-amber';
  };

  return (
    <div className="space-y-6">
      {/* Title & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-1.5 rounded-lg bg-purple-500/20 text-purple-400 border border-purple-500/30">
              <Brain className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-white tracking-tight">Macro-Productivity Vault</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            AI-driven career benchmarking, quantified impact parsing, and skills extraction
          </p>
        </div>

        {/* Quick Sample Action */}
        <button
          onClick={() => setResumeText(SAMPLE_RESUME)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs text-cyan-300 transition-all shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-neon-cyan" />
          <span>Load Senior Architect Resume</span>
        </button>
      </div>

      {/* Upload Zone & Scanner UI */}
      <div className="relative">
        <AnimatePresence mode="wait">
          {!isScanning ? (
            <motion.div
              key="upload-zone"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98 }}
              className={`relative rounded-2xl border-2 border-dashed transition-all p-6 ${
                isDragging
                  ? 'border-neon-cyan bg-cyan-950/20 shadow-glow-cyan'
                  : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'
              }`}
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
            >
              <div className="flex flex-col items-center justify-center text-center space-y-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-purple-500/20 to-cyan-500/20 border border-purple-500/30 flex items-center justify-center">
                  <Upload className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-white">
                    Drag & Drop Resume, or Paste Unstructured Text
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Supports TXT, MD, Markdown or formatted text blocks
                  </p>
                </div>

                <label className="cursor-pointer">
                  <span className="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 transition-all inline-block">
                    Browse File
                  </span>
                  <input
                    type="file"
                    className="hidden"
                    accept=".txt,.md"
                    onChange={handleFileInput}
                  />
                </label>
              </div>

              {/* Text Area for Direct Editing */}
              <div className="mt-4">
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Or paste your resume experience bullets directly here..."
                  rows={4}
                  className="w-full bg-slate-950/70 border border-slate-800 rounded-xl px-4 py-3 text-xs text-slate-200 font-mono placeholder-slate-600 focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/30 transition-all resize-none"
                />
              </div>

              {error && (
                <div className="mt-2 text-xs text-red-400 font-medium flex items-center space-x-1.5">
                  <span>⚠️ {error}</span>
                </div>
              )}

              {/* Trigger Button */}
              <div className="mt-4 flex justify-end">
                <button
                  onClick={handleAnalyze}
                  disabled={!resumeText.trim()}
                  className="flex items-center space-x-2 px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 disabled:opacity-40 text-white text-xs font-semibold shadow-glow-cyan transition-all"
                >
                  <Cpu className="w-4 h-4" />
                  <span>Execute AI Resume NLU</span>
                  <ArrowRight className="w-4 h-4 ml-1" />
                </button>
              </div>
            </motion.div>
          ) : (
            /* Sleek Neural Scanning Document Animation State */
            <motion.div
              key="scanning-state"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel-elevated rounded-2xl p-8 relative overflow-hidden border border-cyan-500/40 shadow-glow-cyan"
            >
              {/* Laser Sweep Line */}
              <motion.div
                variants={scanLaserVariants}
                animate="scan"
                className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-neon-cyan to-transparent shadow-[0_0_20px_#00F0FF] z-20 pointer-events-none"
              />

              <div className="flex flex-col items-center justify-center text-center space-y-4 relative z-10">
                <div className="relative">
                  <div className="w-16 h-16 rounded-2xl bg-cyan-950/60 border border-neon-cyan/50 flex items-center justify-center">
                    <FileCheck className="w-8 h-8 text-neon-cyan animate-pulse" />
                  </div>
                  <motion.div
                    className="absolute -inset-2 rounded-2xl border border-purple-500/40"
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 6, ease: 'linear' }}
                  />
                </div>

                <div>
                  <h3 className="text-base font-bold text-white tracking-wide">
                    Neural Document Scanner Active
                  </h3>
                  <p className="text-xs text-cyan-300 font-mono mt-1">
                    Parsing syntax • Vectorizing skills • Benchmarking quantified impact metrics
                  </p>
                </div>

                {/* Progress bar */}
                <div className="w-64 h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                  <motion.div
                    className="h-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500"
                    style={{ width: `${scanProgress}%` }}
                    transition={{ ease: 'easeOut' }}
                  />
                </div>
                <span className="text-xs font-mono text-slate-400">{scanProgress}% ANALYZED</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Extracted Structured Results Visualizer */}
      <AnimatePresence>
        {analysis && (
          <motion.div
            key={analysis.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="space-y-6"
          >
            {/* Top Stat Row: Candidate & Score Gauge */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Score Gauge Card */}
              <div className="glass-panel rounded-2xl p-5 border border-slate-800 relative overflow-hidden flex items-center space-x-5">
                <div className="relative w-20 h-20 flex-shrink-0 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-800"
                      strokeWidth="3.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <motion.path
                      className="text-neon-cyan"
                      strokeDasharray={`${analysis.overall_score}, 100`}
                      strokeWidth="3.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      initial={{ strokeDasharray: '0, 100' }}
                      animate={{ strokeDasharray: `${analysis.overall_score}, 100` }}
                      transition={{ duration: 1.2, ease: 'easeOut' }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-xl font-black font-mono ${getScoreColor(analysis.overall_score)}`}>
                      {Math.round(analysis.overall_score)}
                    </span>
                    <span className="text-[9px] text-slate-500 font-mono">/ 100</span>
                  </div>
                </div>

                <div>
                  <div className="flex items-center space-x-1.5">
                    <Award className="w-4 h-4 text-neon-cyan" />
                    <span className="text-xs font-semibold text-slate-300">Executive Index</span>
                  </div>
                  <h4 className="text-sm font-bold text-white mt-1">
                    {analysis.overall_score >= 80
                      ? 'Enterprise Ready (Top Tier)'
                      : analysis.overall_score >= 60
                      ? 'Competitive Candidate'
                      : 'Developing Profile'}
                  </h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Measured across metric density & tech breadth
                  </p>
                </div>
              </div>

              {/* Candidate Info Card */}
              <div className="glass-panel rounded-2xl p-5 border border-slate-800 md:col-span-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-purple-400 uppercase tracking-wider">
                      Identified Candidate
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono">
                      {new Date(analysis.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mt-1">
                    {analysis.candidate_name || 'Senior Software Engineer'}
                  </h3>
                  <p className="text-xs text-slate-300 mt-1 line-clamp-2 leading-relaxed">
                    {analysis.summary}
                  </p>
                </div>

                <div className="flex items-center space-x-4 mt-3 pt-3 border-t border-slate-800/80 text-xs">
                  <div className="flex items-center space-x-1.5 text-slate-300">
                    <TrendingUp className="w-3.5 h-3.5 text-neon-emerald" />
                    <span>
                      <strong className="text-white">{analysis.metrics.length}</strong> Impact Metrics
                    </span>
                  </div>
                  <div className="flex items-center space-x-1.5 text-slate-300">
                    <Layers className="w-3.5 h-3.5 text-neon-cyan" />
                    <span>
                      <strong className="text-white">
                        {analysis.skills.reduce((acc, cat) => acc + cat.skills.length, 0)}
                      </strong>{' '}
                      Skills Classified
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Categorized Skills Section */}
            <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Code2 className="w-4 h-4 text-neon-cyan" />
                  <h3 className="text-sm font-bold text-white">Extracted Skill Matrix</h3>
                </div>
                <span className="text-xs font-mono text-slate-500">Categorized by Domain</span>
              </div>

              <motion.div
                variants={staggerContainerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                {analysis.skills.map((categoryGroup) => (
                  <div
                    key={categoryGroup.category}
                    className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-2"
                  >
                    <span className="text-xs font-semibold text-cyan-300 tracking-wide flex items-center space-x-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-neon-cyan" />
                      <span>{categoryGroup.category}</span>
                    </span>

                    <div className="flex flex-wrap gap-1.5">
                      {categoryGroup.skills.map((skill) => (
                        <motion.span
                          key={skill}
                          variants={skillBadgeVariants}
                          whileHover="hover"
                          className="px-2.5 py-1 rounded-md text-[11px] font-mono font-medium bg-slate-800 text-slate-200 border border-slate-700/60 hover:border-cyan-400/80 hover:text-white transition-all cursor-default"
                        >
                          {skill}
                        </motion.span>
                      ))}
                    </div>
                  </div>
                ))}
              </motion.div>
            </div>

            {/* Quantified Metrics Section */}
            <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-neon-emerald" />
                  <h3 className="text-sm font-bold text-white">High-Impact Quantified Metrics</h3>
                </div>
                <span className="text-xs font-mono text-slate-500">Extracted Achievements</span>
              </div>

              <div className="grid grid-cols-1 gap-2.5">
                {analysis.metrics.map((m, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.08 }}
                    className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start justify-between gap-3 hover:border-slate-700 transition-all"
                  >
                    <div className="flex items-start space-x-3">
                      <div className="p-1 rounded-md bg-emerald-500/10 text-emerald-400 mt-0.5">
                        <CheckCircle2 className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs text-slate-200 font-medium leading-relaxed">
                          {m.metric}
                        </p>
                        <span className="inline-block mt-1 text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                          Category: {m.category}
                        </span>
                      </div>
                    </div>

                    <div className="flex-shrink-0">
                      <span className="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 font-mono font-bold text-xs border border-emerald-500/30">
                        {m.quantified_value}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
