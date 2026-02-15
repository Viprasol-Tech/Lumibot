import { useState, useEffect } from "react";
import { fetchSettings, updateSettings } from "../services/api";

export default function Settings() {
  const [form, setForm] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetchSettings().then(setForm);
  }, []);

  if (!form) return <p className="text-gray-500">Loading...</p>;

  const handleChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    await updateSettings(form);
    setSaved(true);
  };

  const fields = [
    { key: "symbol", label: "Symbol", type: "text" },
    { key: "risk_per_trade", label: "Risk Per Trade (%)", type: "number", step: 0.005 },
    { key: "max_positions", label: "Max Positions", type: "number", step: 1 },
    { key: "stop_loss_pct", label: "Stop Loss (%)", type: "number", step: 0.005 },
    { key: "take_profit_pct", label: "Take Profit (%)", type: "number", step: 0.005 },
    { key: "trailing_stop_pct", label: "Trailing Stop (%)", type: "number", step: 0.005 },
  ];

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Strategy Settings</h2>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6 max-w-lg space-y-4">
        {fields.map((f) => (
          <div key={f.key}>
            <label className="block text-xs text-gray-400 mb-1">{f.label}</label>
            <input
              type={f.type}
              step={f.step}
              value={form[f.key] ?? ""}
              onChange={(e) =>
                handleChange(
                  f.key,
                  f.type === "number" ? parseFloat(e.target.value) : e.target.value
                )
              }
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-500"
            />
          </div>
        ))}

        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={form.use_trailing_stop}
            onChange={(e) => handleChange("use_trailing_stop", e.target.checked)}
            className="accent-emerald-500"
          />
          <label className="text-sm text-gray-300">Use Trailing Stop</label>
        </div>

        <button
          onClick={handleSave}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded text-sm font-medium"
        >
          Save Settings
        </button>
        {saved && <p className="text-emerald-400 text-xs mt-1">Settings saved!</p>}
      </div>
    </div>
  );
}
