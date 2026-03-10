// 🎯 Add this import line
import { useState, useEffect, useRef } from 'react'; 
import api from '../services/api';

// src/hooks/useLiveMatches.ts
export function useLiveMatches() {
  const [matches, setMatches] = useState<LiveMatch[]>([]);
  const [status, setStatus] = useState<'fresh' | 'revalidating' | 'loading'>('loading');
  const [lastSync, setLastSync] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollingRef = useRef<any>(null);

  const fetchMatches = async () => {
    try {
      const response = await api.get('/upcoming/sync');
      
      // 🎯 Target the new object structure
      setMatches(response.data.matches || []);
      setStatus(response.data.status);
      setLastSync(response.data.last_sync);
      
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch live matches");
    }
  };

   useEffect(() => {
  fetchMatches();

  if (status === 'revalidating' && !pollingRef.current) {
    console.log("🚀 Starting single poll instance");
    pollingRef.current = setInterval(() => {
      fetchMatches();
    }, 3000);
  }

  if (status === 'fresh' && pollingRef.current) {
    console.log("🛑 Killing poll - Data is fresh");
    clearInterval(pollingRef.current);
    pollingRef.current = null;
  }

  return () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  };
}, [status]);

  

  return { matches, status, lastSync, error, refetch: fetchMatches };
}
