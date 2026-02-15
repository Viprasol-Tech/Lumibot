import useFetch from "../hooks/useFetch";
import { fetchOverview } from "../services/api";

function Card({ label, value, color = "text-white" }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
      <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
      <p className={`text-2xl font-semibold mt-1 ${color}`}>{value}</p>
    </div>
  );
}

export default function Overview() {
  const { data, loading } = useFetch(fetchOverview);

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (!data) return <p className="text-red-400">Failed to load overview</p>;

  const pnlColor = data.daily_pnl >= 0 ? "text-emerald-400" : "text-red-400";

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Dashboard Overview</h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card label="Account Value" value={`$${data.account_value.toLocaleString()}`} />
        <Card label="Daily P&L" value={`$${data.daily_pnl.toLocaleString()}`} color={pnlColor} />
        <Card label="Open Positions" value={data.open_positions} />
        <Card
          label="Bot Status"
          value={data.bot_status.toUpperCase()}
          color={data.bot_status === "running" ? "text-emerald-400" : "text-yellow-400"}
        />
      </div>
    </div>
  );
}
