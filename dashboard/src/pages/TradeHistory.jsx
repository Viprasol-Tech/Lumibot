import useFetch from "../hooks/useFetch";
import { fetchTrades } from "../services/api";

export default function TradeHistory() {
  const { data, loading } = useFetch(fetchTrades);

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Trade History</h2>
      {!data?.length ? (
        <p className="text-gray-500">No trades yet</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-gray-400 border-b border-gray-800">
              <tr>
                <th className="text-left p-2">Time</th>
                <th className="text-left p-2">Symbol</th>
                <th className="text-left p-2">Side</th>
                <th className="text-right p-2">Qty</th>
                <th className="text-right p-2">Price</th>
                <th className="text-right p-2">P&L</th>
              </tr>
            </thead>
            <tbody>
              {data.map((t) => (
                <tr key={t.id} className="border-b border-gray-800/50 hover:bg-gray-900">
                  <td className="p-2 text-gray-400">
                    {new Date(t.created_at).toLocaleString()}
                  </td>
                  <td className="p-2 font-medium">{t.symbol}</td>
                  <td
                    className={`p-2 uppercase ${
                      t.side === "buy" ? "text-emerald-400" : "text-red-400"
                    }`}
                  >
                    {t.side}
                  </td>
                  <td className="p-2 text-right">{t.quantity}</td>
                  <td className="p-2 text-right">${t.price.toFixed(2)}</td>
                  <td
                    className={`p-2 text-right font-medium ${
                      t.pnl >= 0 ? "text-emerald-400" : "text-red-400"
                    }`}
                  >
                    ${t.pnl.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
