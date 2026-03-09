import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { WeeklyPoint } from '../../types/lab';

export function EquityChart({ data }: { data: WeeklyPoint[] }) {
  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl h-[400px]">
      <h3 className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-6">
        Weekly Equity Curve (USD)
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis 
            dataKey="date" 
            stroke="#475569" 
            fontSize={12} 
            tickMargin={10}
            tickFormatter={(str) => str.split('-').slice(1).join('/')} // 2025-01-01 -> 01/01
          />
          <YAxis 
            stroke="#475569" 
            fontSize={12} 
            domain={['dataMin - 50', 'dataMax + 50']} 
            tickFormatter={(val) => `$${val}`}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
            itemStyle={{ color: '#22c55e' }}
            labelStyle={{ color: '#64748b', marginBottom: '4px' }}
          />
          <Line 
            type="monotone" 
            dataKey="balance" 
            stroke="#22c55e" 
            strokeWidth={2} 
            dot={false}
            activeDot={{ r: 4, strokeWidth: 0 }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
