import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import useFetch from "../hooks/useFetch";
import { fetchPnl } from "../services/api";

export default function PnLChart() {
  const { data, loading } = useFetch(fetchPnl);

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (!data?.length) return <p className="text-gray-500">No P&L data yet</p>;

  const chartData = data.map((r) => ({
    date: new Date(r.date).toLocaleDateString(),
    value: r.portfolio_value,
    pnl: r.cumulative_pnl,
  }));

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Equity Curve</h2>
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4" style={{ height: 400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="date" stroke="#6b7280" fontSize={12} />
            <YAxis stroke="#6b7280" fontSize={12} tickFormatter={(v) => `$${v.toLocaleString()}`} />
            <Tooltip
              contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151" }}
              labelStyle={{ color: "#9ca3af" }}
            />
            <Area type="monotone" dataKey="value" stroke="#10b981" fill="url(#grad)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
