import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from "recharts";

export function MonthlyBreakdown({ data }: { data: any[] }) {
  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl h-[400px]">
      <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-6">
        Monthly Profit & Loss (GBP)
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#1e293b"
            vertical={false}
          />
          <XAxis
            dataKey="month"
            stroke="#475569"
            fontSize={12}
            tickMargin={10}
          />
          <YAxis
            stroke="#475569"
            fontSize={12}
            // 🎯 Format Y-Axis: $100 -> $100.00
            tickFormatter={(val) =>
              `$${Number(val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            }
          />

          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0];
                const value = Number(data.value);
                const isPositive = value >= 0;

                return (
                  <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg shadow-2xl">
                    <p className="text-[10px] text-slate-500 font-bold uppercase mb-1">
                      {data.payload.month}
                    </p>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-300">
                        Net Profit:
                      </span>
                      <span
                        className="text-sm font-mono font-bold"
                        style={{ color: isPositive ? "#22c55e" : "#ef4444" }} // 🎯 FORCED COLOR
                      >
                        $
                        {value.toLocaleString(undefined, {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </span>
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />

          <ReferenceLine y={0} stroke="#475569" />
          <Bar dataKey="profit" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.profit >= 0 ? "#22c55e" : "#ef4444"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
