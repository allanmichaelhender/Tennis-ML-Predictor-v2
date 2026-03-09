// 🎯 This matches your FastAPI 'PerformanceSummary'
export interface PerformanceSummary {
  roi: number;
  total_profit: number;
  win_rate: number;
  brier_score: number;
  total_bets: number;
}

// 🎯 This matches your 'WeeklyPoint'
export interface WeeklyPoint {
  date: string;
  balance: number;
}

// 🎯 The big response object
export interface ModelPerformanceResponse {
  summary: PerformanceSummary;
  equity_curve: WeeklyPoint[];
  monthly_breakdown: any[]; // We'll use 'any' for now to keep it simple
}
