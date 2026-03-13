import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import type { WeeklyPoint } from "../../types/lab";

export function EquityChart({ data }: { data: WeeklyPoint[] }) {
  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl h-[400px] w-full">
      <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-6">
        Performance Trajectory (GBP)
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#1e293b"
            vertical={false}
          />
          <XAxis
            dataKey="date"
            stroke="#475569"
            fontSize={12}
            tickMargin={10}
            tickFormatter={(str) => str.split("-").slice(1).join("/")} // 2025-01-01 -> 01/01
          />
          <YAxis
            stroke="#475569"
            fontSize={12}
            domain={["dataMin - 20", "dataMax + 20"]}
            // 🎯 Format Y-Axis: $1112.432 -> $1,112.43
            tickFormatter={(val) =>
              `£${Number(val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            }
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a", // Dark background
              border: "1px solid #1e293b", // Slate border
              borderRadius: "8px",
            }}
            labelStyle={{
              color: "#94a3b8",
              fontWeight: "bold",
              marginBottom: "4px",
            }} // 🎯 Muted Slate for "55-60%"
            itemStyle={{ color: "#22c55e", fontSize: "12px" }}
            // 🎯 Format Hover Popup: 1112.432 -> $1,112.43
            formatter={(value: any, name: any, props: any) => {
              const { payload } = props;

              if (name === "avg_predicted") {
                return [
                  `${(Number(value) * 100).toFixed(1)}%`,
                  "Model Confidence",
                ];
              }
              if (name === "actual_win_rate") {
                return [
                  `${(Number(value) * 100).toFixed(1)}%`,
                  `Actual Win Rate (${payload.match_count} matches)`,
                ];
              }
              return [value, name];
            }}
          />
          <Area
            type="monotone"
            dataKey="balance"
            stroke="#22c55e"
            fillOpacity={1}
            fill="url(#colorBalance)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
