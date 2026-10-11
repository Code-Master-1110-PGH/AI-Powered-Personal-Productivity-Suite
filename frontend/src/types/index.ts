export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface SkillCategory {
  category: string;
  skills: string[];
}

export interface QuantifiedMetric {
  metric: string;
  category: string;
  quantified_value: string;
}

export interface ResumeAnalysis {
  id: number;
  user_id: number;
  candidate_name?: string;
  summary?: string;
  skills: SkillCategory[];
  metrics: QuantifiedMetric[];
  overall_score: number;
  created_at: string;
  updated_at: string;
}

export type TaskStatus = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  raw_prompt?: string;
  status: TaskStatus;
  priority: TaskPriority;
  estimated_duration_minutes: number;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface DailySchedule {
  id: number;
  user_id: number;
  task_id?: number;
  scheduled_date: string;
  start_time: string;
  end_time: string;
  time_block_title: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
  task?: Task;
}

export interface DailyItineraryResponse {
  user_id: number;
  scheduled_date: string;
  total_blocks: number;
  itinerary: DailySchedule[];
}

export interface ExtractedTaskIntent {
  raw_input: string;
  intent: string;
  extracted_title: string;
  priority: TaskPriority;
  target_start_time: string;
  target_end_time: string;
  duration_minutes: number;
  confidence_score: number;
}

export interface SmartTaskResponse {
  message: string;
  task: Task;
  schedule: DailySchedule;
  nlu_metadata: ExtractedTaskIntent;
}

