import { Routes, Route, NavLink } from "react-router-dom";
import Overview from "./pages/Overview";
import Positions from "./pages/Positions";
import TradeHistory from "./pages/TradeHistory";
import PnLChart from "./pages/PnLChart";
import BotControls from "./pages/BotControls";
import Settings from "./pages/Settings";

const navItems = [
  { to: "/", label: "Overview" },
  { to: "/positions", label: "Positions" },
  { to: "/trades", label: "Trades" },
  { to: "/pnl", label: "P&L" },
  { to: "/controls", label: "Controls" },
  { to: "/settings", label: "Settings" },
];

export default function App() {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <nav className="w-56 bg-gray-900 border-r border-gray-800 p-4 flex flex-col gap-1">
        <h1 className="text-lg font-bold text-emerald-400 mb-6">Trading Bot</h1>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `px-3 py-2 rounded text-sm ${
                isActive
                  ? "bg-emerald-600 text-white"
                  : "text-gray-400 hover:text-white hover:bg-gray-800"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Main content */}
      <main className="flex-1 p-6 overflow-auto">
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/positions" element={<Positions />} />
          <Route path="/trades" element={<TradeHistory />} />
          <Route path="/pnl" element={<PnLChart />} />
          <Route path="/controls" element={<BotControls />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}
