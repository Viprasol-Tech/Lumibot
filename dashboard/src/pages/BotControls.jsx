import { useState } from "react";
import useFetch from "../hooks/useFetch";
import { fetchBotStatus, controlBot } from "../services/api";

export default function BotControls() {
  const { data, loading, reload } = useFetch(fetchBotStatus);
  const [busy, setBusy] = useState(false);

  const handleAction = async (action) => {
    setBusy(true);
    try {
      await controlBot(action);
      reload();
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  const statusColor =
    data?.status === "running"
      ? "text-emerald-400"
      : data?.status === "paused"
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Bot Controls</h2>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6 max-w-md">
        <p className="text-sm text-gray-400 mb-1">Current Status</p>
        <p className={`text-3xl font-bold mb-1 ${statusColor}`}>
          {data?.status?.toUpperCase() ?? "UNKNOWN"}
        </p>
        <p className="text-xs text-gray-500 mb-6">Mode: {data?.mode?.toUpperCase()}</p>

        <div className="flex gap-3">
          <button
            disabled={busy || data?.status === "running"}
            onClick={() => handleAction("start")}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 rounded text-sm font-medium"
          >
            Start
          </button>
          <button
            disabled={busy || data?.status === "paused"}
            onClick={() => handleAction("pause")}
            className="px-4 py-2 bg-yellow-600 hover:bg-yellow-500 disabled:opacity-40 rounded text-sm font-medium"
          >
            Pause
          </button>
          <button
            disabled={busy || data?.status === "stopped"}
            onClick={() => handleAction("stop")}
            className="px-4 py-2 bg-red-600 hover:bg-red-500 disabled:opacity-40 rounded text-sm font-medium"
          >
            Stop
          </button>
        </div>
      </div>
    </div>
  );
}
