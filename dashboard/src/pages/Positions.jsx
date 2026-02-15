import useFetch from "../hooks/useFetch";
import { fetchPositions } from "../services/api";

export default function Positions() {
  const { data, loading } = useFetch(fetchPositions);

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Open Positions</h2>
      {!data?.length ? (
        <p className="text-gray-500">No open positions</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-gray-400 border-b border-gray-800">
              <tr>
                <th className="text-left p-2">Symbol</th>
                <th className="text-left p-2">Type</th>
                <th className="text-right p-2">Qty</th>
                <th className="text-right p-2">Entry</th>
                <th className="text-right p-2">Current</th>
                <th className="text-right p-2">P&L</th>
              </tr>
            </thead>
            <tbody>
              {data.map((pos) => (
                <tr key={pos.id} className="border-b border-gray-800/50 hover:bg-gray-900">
                  <td className="p-2 font-medium">{pos.symbol}</td>
                  <td className="p-2 text-gray-400">{pos.asset_type}</td>
                  <td className="p-2 text-right">{pos.quantity}</td>
                  <td className="p-2 text-right">${pos.entry_price.toFixed(2)}</td>
                  <td className="p-2 text-right">${pos.current_price.toFixed(2)}</td>
                  <td
                    className={`p-2 text-right font-medium ${
                      pos.unrealized_pnl >= 0 ? "text-emerald-400" : "text-red-400"
                    }`}
                  >
                    ${pos.unrealized_pnl.toFixed(2)}
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
