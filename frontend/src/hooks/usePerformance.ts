import { useState, useEffect } from 'react';
import api from '../services/api';
import type { ModelPerformanceResponse } from '../types/lab';

export function usePerformance() {
  const [data, setData] = useState<ModelPerformanceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPerformance = async () => {
    try {
      setLoading(true);
      const response = await api.get<ModelPerformanceResponse>('/lab/model-performance');
      setData(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch performance data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPerformance();
  }, []);

  return { data, loading, error, refetch: fetchPerformance };
}
